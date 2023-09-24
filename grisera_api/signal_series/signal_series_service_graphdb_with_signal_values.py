from typing import List, Union, Optional

from starlette.datastructures import QueryParams

from models.not_found_model import NotFoundByIdModel
from signal_series.ss_helpers import get_node_property
from signal_series.signal_series_model import Type, SignalSeriesIn, SignalSeriesOut, SignalIn, SignalValueNodesIn, \
    StampNodesIn, SignalSeriesNodesOut, BasicSignalSeriesOut, SignalSeriesTransformationIn, \
    SignalSeriesTransformationRelationshipIn, SignalSeriesMultidimensionalOut
from signal_series.signal_series_service_graphdb import SignalSeriesServiceGraphDB
from signal_series.transformation.SignalSeriesTransformationFactory import SignalSeriesTransformationFactory
from signal_series.transformation.multidimensional.SignalSeriesTransformationMultidimensional import \
    SignalSeriesTransformationMultidimensional


class SignalSeriesServiceGraphDBWithSignalValues(SignalSeriesServiceGraphDB):

    def __init__(self, property_stamp_name, label_stamp_name, signal_series_type):
        self.graphdb_service = None
        self.property_stamp_name = property_stamp_name
        self.label_stamp_name = label_stamp_name
        self.signal_series_type = signal_series_type
        self.frequency_graphdb_with_signals_service = None

    def save_signal_series(self, signal_series: SignalSeriesIn):
        """
        Send request to graph api to create new time series
        Args:
            signal_series (SignalSeriesIn): Time series to be added
        Returns:
            Result of request as time series object
        """
        result = self.graphdb_service.save_signal_series(signal_series)
        if result.errors is not None:
            return result

        signal_series_id = result.id

        errors = self.save_signal_values(signal_series.signal_values, signal_series_id,
                                         self.get_experiment_id(signal_series_id), signal_series.type)
        if errors is not None:
            return SignalSeriesOut(**signal_series.dict(), errors=errors)

        result.signal_values = self.get_signal_values(
            signal_series_id, signal_series.type)

        return result

    def transform_signal_series(self, signal_series_transformation: SignalSeriesTransformationIn):
        """
        Send request to graph api to create new transformed time series

        Args:
            signal_series_transformation (SignalSeriesTransformationIn): Time series transformation parameters

        Returns:
            Result of request as time series object
        """
        source_signal_series = []
        for signal_series_id in signal_series_transformation.source_signal_series_ids:
            signal_series = self.get_signal_series(signal_series_id)
            if signal_series.errors is not None:
                return signal_series
            source_signal_series.append(signal_series)
        try:
            new_signal_series, new_signal_values_id_mapping = SignalSeriesTransformationFactory().get_transformation(
                signal_series_transformation.name) \
                .transform(source_signal_series, signal_series_transformation.additional_properties)
        except Exception as e:
            return SignalSeriesNodesOut(errors=str(e))
        new_signal_series.measure_id = signal_series_transformation.destination_measure_id
        new_signal_series.observable_information_id = signal_series_transformation.destination_observable_information_id

        if(new_signal_series.type == Type.frequencystamp):
            service_to_handle_new_signal = self.frequency_graphdb_with_signals_service
            result = self.frequency_graphdb_with_signals_service.save_signal_series(new_signal_series)
        else: 
            service_to_handle_new_signal = self
            result = self.save_signal_series(new_signal_series)
            assert len(new_signal_values_id_mapping) == len(
                result.signal_values), "transformation Signal_Values mapping does not have correct length"
            for signal_value_ids, new_signal_value in zip(new_signal_values_id_mapping, result.signal_values):
                new_signal_value_id = new_signal_value["signal_value"]["id"]
                for index, old_signal_value_id in enumerate(signal_value_ids):
                    relationship = self.graph_api_service.create_relationships(new_signal_value_id, old_signal_value_id,
                                                                            "basedOn")
                    self.graph_api_service.create_relationship_properties(relationship["id"],
                                                                        SignalSeriesTransformationRelationshipIn(
                                                                            additional_properties=[
                                                                                {'key': 'order', 'value': index + 1}]))

        for index, signal_series_id in enumerate(signal_series_transformation.source_signal_series_ids):
            relationship = service_to_handle_new_signal.graph_api_service.create_relationships(
                result.id, signal_series_id, "transformedFrom")
            service_to_handle_new_signal.graph_api_service.create_relationship_properties(relationship["id"],
                                                                  SignalSeriesTransformationRelationshipIn(
                                                                      additional_properties=[
                                                                          {'key': 'order', 'value': index + 1}]))

        return result

    def get_experiment_id(self, signal_series_id: int):
        query = {
            "nodes": [
                {
                    "id": signal_series_id,
                    "label": self.signal_series_type
                },
                {
                    "label": "Observable_Information"
                },
                {
                    "label": "Recording"
                },
                {
                    "label": "Participation"
                },
                {
                    "label": "Activity Execution"
                },
                {
                    "label": "Activity Execution"
                },
                {
                    "label": "Experiment",
                    "result": True
                }
            ],
            "relations": [
                {
                    "begin_node_index": 0,
                    "end_node_index": 1,
                    "label": "hasObservableInformation"
                },
                {
                    "begin_node_index": 1,
                    "end_node_index": 2,
                    "label": "hasRecording"
                },
                {
                    "begin_node_index": 2,
                    "end_node_index": 3,
                    "label": "hasParticipation"
                },
                {
                    "begin_node_index": 3,
                    "end_node_index": 4,
                    "label": "hasActivityExecution"
                },
                {
                    "begin_node_index": 5,
                    "end_node_index": 4,
                    "label": "nextActivityExecution",
                    "min_count": 0
                },
                {
                    "begin_node_index": 6,
                    "end_node_index": 5,
                    "label": "hasScenario"
                },
            ]
        }
        response = self.graph_api_service.get_nodes_by_query(query)
        for row in response["rows"]:
            return row[0]["id"]
        return None

    def get_neighbour_node_id(self, node_id: int, relation_name: str, forward: bool = True):
        relations_response = self.graph_api_service.get_node_relationships(
            node_id)
        for relation in relations_response["relationships"]:
            if relation["name"] == relation_name:
                if relation["start_node" if forward else "end_node"] == node_id:
                    return relation["end_node" if forward else "start_node"], relation["id"]
        return None, None

    def get_neighbour_node(self, node_id: int, relation_name: str, forward: bool = True):
        neighbour_node_id, relation_id = self.get_neighbour_node_id(
            node_id, relation_name, forward)
        if neighbour_node_id is not None:
            get_response = self.graph_api_service.get_node(neighbour_node_id)
            if get_response["errors"] is None:
                return get_response, relation_id
        return None, None

    def get_or_create_stamp_node(self, stamp_value: int, stamp):
        if stamp_value is None:
            return {"errors": "" + self.label_stamp_name + "value is None. Please check " + self.signal_series_type + "type."}
        previous_stamp_id = None
        previous_stamp_stamp_relation_id = None
        while stamp is not None and int(get_node_property(stamp, self.property_stamp_name)) < stamp_value:
            previous_stamp_id = stamp["id"]
            stamp, previous_stamp_stamp_relation_id = self.get_neighbour_node(
                stamp["id"], "next")

        if stamp is None or int(get_node_property(stamp, self.property_stamp_name)) != stamp_value:
            new_stamp_node = self.graph_api_service.create_node(
                self.label_stamp_name)

            if new_stamp_node["errors"] is not None:
                return new_stamp_node

            new_stamp_id = new_stamp_node["id"]

            stamp_properties_response = self.graph_api_service.create_properties(new_stamp_id,
                                                                                 self.get_stamp_nodes_in(stamp_value))
            if stamp_properties_response["errors"] is not None:
                return stamp_properties_response

            if previous_stamp_id is not None:
                self.graph_api_service.create_relationships(start_node=previous_stamp_id,
                                                            end_node=new_stamp_id,
                                                            name="next")
            if stamp is not None:
                self.graph_api_service.create_relationships(start_node=new_stamp_id,
                                                            end_node=stamp["id"],
                                                            name="next")
            if previous_stamp_stamp_relation_id is not None:
                self.graph_api_service.delete_relationship(
                    previous_stamp_stamp_relation_id)

            return self.graph_api_service.get_node(new_stamp_id)
        return stamp

    def create_signal_value(self, signal_value: SignalValueNodesIn, previous_signal_value_node, signal_series_id: int):
        signal_value_node_response = self.graph_api_service.create_node(
            "Signal_Value")

        if signal_value_node_response["errors"] is not None:
            return signal_value_node_response

        signal_value_properties_response = self.graph_api_service.create_properties(signal_value_node_response["id"],
                                                                                    signal_value)
        if signal_value_properties_response["errors"] is not None:
            return signal_value_properties_response

        if previous_signal_value_node is None:
            self.graph_api_service.create_relationships(start_node=signal_series_id,
                                                        end_node=signal_value_node_response["id"],
                                                        name="hasSignal")
        else:
            self.graph_api_service.create_relationships(start_node=previous_signal_value_node["id"],
                                                        end_node=signal_value_node_response["id"],
                                                        name="next")

        return signal_value_node_response

    def save_signal_values(self, signal_values: List[SignalIn], signal_series_id: int, experiment_id: int,
                           stamp_type: Type):

        stamp, experiment_stamp_relation_id = self.get_neighbour_node(experiment_id, "takes") \
            if experiment_id is not None else (None, None)
        signal_value_node = None

        for signal_value in signal_values:
            current_signal_value_node = self.create_signal_value(signal_value.signal_value, signal_value_node,
                                                                 signal_series_id)

            if current_signal_value_node["errors"] is not None:
                return current_signal_value_node

            current_stamp = self.get_current_stamp(
                stamp_type, signal_value, stamp)

            if current_stamp["errors"] is not None:
                return current_stamp["errors"]

            if signal_value_node is None and (
                    stamp is None or self.get_stamp_value(get_node_property(current_stamp, self.property_stamp_name)) < self.get_stamp_value(
                    get_node_property(stamp, self.property_stamp_name))):
                if experiment_stamp_relation_id is not None:
                    self.graph_api_service.delete_relationship(
                        experiment_stamp_relation_id)
                if experiment_id is not None:
                    self.graph_api_service.create_relationships(start_node=experiment_id,
                                                                end_node=current_stamp["id"],
                                                                name="takes")

            current_stamp = self.create_relation_nodes(
                stamp_type, current_signal_value_node, signal_value, current_stamp)
            if current_stamp["errors"] is not None:
                return current_stamp["errors"]

            stamp = current_stamp
            signal_value_node = current_signal_value_node
        return None

    def get_signal_series(self, signal_series_id: Union[int, str], depth: int = 0,
                          signal_min_value: Optional[int] = None,
                          signal_max_value: Optional[int] = None):
        """
        Send request to graph api to get given time series
        Args:
            signal_series_id (int | str): identity of time series
            depth: (int): specifies how many related entities will be traversed to create the response
            signal_min_value (Optional[int]): Filter Signal_Values by min value
            signal_max_value (Optional[int]): Filter Signal_Values by max value
        Returns:
            Result of request as time series object
        """
        signal_series = self.graphdb_service.get_signal_series(
            signal_series_id, depth)
        if signal_series.errors is None:
            signal_series.signal_values = self.get_signal_values(signal_series_id, signal_series.type,
                                                                 signal_min_value, signal_max_value)
        return signal_series

    def get_signal_series_multidimensional(self, signal_series_ids: List[Union[int, str]]):
        """
        Send request to graph api to get given time series
        Args:
            signal_series_ids (int | str): Ids of the time series
        Returns:
            Result of request as time series object
        """
        source_signal_series = []
        for signal_series_id in signal_series_ids:
            signal_series = self.get_signal_series(signal_series_id)
            if signal_series.errors is not None:
                return signal_series
            source_signal_series.append(signal_series)
        try:
            result = SignalSeriesTransformationMultidimensional().transform(source_signal_series)
            for signal_series in source_signal_series:
                signal_series.signal_values = []
            result.signal_series = source_signal_series
            return result
        except Exception as e:
            return SignalSeriesMultidimensionalOut(errors=str(e))

    def get_signal_values(self, signal_series_id: Union[int, str], signal_series_type: str,
                          signal_min_value: Optional[int] = None,
                          signal_max_value: Optional[int] = None):
        """
        Send requests to graph api to get all Signal_Values
        Args:
            signal_series_id (int | str): identity of the time series
            signal_series_type (str): type of the time series
            signal_min_value (Optional[int]): Filter Signal_Values by min value
            signal_max_value (Optional[int]): Filter Signal_Values by max value
        Returns:
            Array of Signal_Value objects
        """
        raise Exception("get_signal_values not implemented yet")

    def get_signal_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        query = {
            "nodes": [
                {
                    "label": self.signal_series_type,
                    "result": True
                },
            ],
            "relations": [
            ]
        }
        params_per_node = {}
        for param_key, param_value in dict(params).items():
            if "_" in param_key:
                param_key_prefix, param_key_suffix = param_key.split("_", 1)
                if param_key_prefix not in params_per_node:
                    params_per_node[param_key_prefix] = []
                params_per_node[param_key_prefix].append({
                    "key": param_key_suffix,
                    "operator": "equals",
                    "value": param_value
                })
            else:
                print("Bad query param value format")

        def get_or_append_node_to_query(query, node_indexes, label, id=None, parameters=None):
            if label in node_indexes:
                return node_indexes[label]
            new_node = {"label": label}
            if id is not None:
                new_node["id"] = id
            if parameters is not None:
                new_node["parameters"] = parameters
            new_node_index = len(query["nodes"])
            node_indexes[label] = new_node_index
            query["nodes"].append(new_node)
            if label == "Observable_Information":
                query["relations"].append({
                    "begin_node_index": 0,
                    "end_node_index": new_node_index,
                    "label": "hasObservableInformation"
                })
            elif label == "Recording":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Observable_Information"),
                    "end_node_index": new_node_index,
                    "label": "hasRecording"
                })
            elif label == "Participation":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Recording"),
                    "end_node_index": new_node_index,
                    "label": "hasParticipation"
                })
            elif label == "Participant_State":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Participation"),
                    "end_node_index": new_node_index,
                    "label": "hasParticipantState"
                })
            elif label == "Participant":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Participant_State"),
                    "end_node_index": new_node_index,
                    "label": "hasParticipant"
                })
            elif label == "Activity Execution":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Participation"),
                    "end_node_index": new_node_index,
                    "label": "hasActivityExecution"
                })
            elif label == "Activity":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Activity Execution"),
                    "end_node_index": new_node_index,
                    "label": "hasActivity"
                })
            elif label == "Experiment":
                new_activity_execution_index = len(query["nodes"])
                query["nodes"].append({
                    "label": "Activity Execution"
                })
                query["relations"].append({
                    "begin_node_index": new_activity_execution_index,
                    "end_node_index": get_or_append_node_to_query(query, node_indexes, "Activity Execution"),
                    "label": "nextActivityExecution",
                    "min_count": 0
                })
                query["relations"].append({
                    "begin_node_index": new_node_index,
                    "end_node_index": new_activity_execution_index,
                    "label": "hasScenario"
                })
            elif label == "Registered_Channel":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Recording"),
                    "end_node_index": new_node_index,
                    "label": "hasRegisteredChannel"
                })
            elif label == "Channel":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Registered_Channel"),
                    "end_node_index": new_node_index,
                    "label": "hasChannel"
                })
            elif label == "Registered_Data":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Channel"),
                    "end_node_index": new_node_index,
                    "label": "hasRegisteredData"
                })
            else:
                print("Unknown node label")
            return new_node_index

        node_indexes = {}
        for node_label in ["Observable_Information", "Recording", "Participation", "Participant_State", "Participant",
                           "Activity Execution", "Activity", "Experiment", "Registered_Channel", "Channel",
                           "Registered_Data"]:
            node_param_name = node_label.lower().replace(" ", "")
            if node_param_name in params_per_node:
                node_id = None
                if "id" in params_per_node[node_param_name]:
                    node_id = int(params_per_node[node_param_name]["id"])
                    del params_per_node[node_param_name]["id"]
                get_or_append_node_to_query(
                    query, node_indexes, node_label, node_id, params_per_node[node_param_name])

        response = self.graph_api_service.get_nodes_by_query(query)

        signal_series_nodes = []
        for signal_series_row in response["rows"]:
            signal_series_node = signal_series_row[0]
            properties = {
                'id': signal_series_node['id'], 'additional_properties': []}
            for property in signal_series_node["properties"]:
                if property["key"] in ["type", "source"]:
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append(
                        {'key': property['key'], 'value': property['value']})
            signal_series = BasicSignalSeriesOut(**properties)
            signal_series_nodes.append(signal_series)

        return SignalSeriesNodesOut(signal_series_nodes=signal_series_nodes)

    def delete_signal_series(self, signal_series_id: int):
        """
        Send request to graph api to delete given time series

        Args:
            signal_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        raise Exception("delete_signal_series not implemented yet")

    def get_stamp_nodes_in(self, stamp_value):
        raise Exception("get_stamp_nodes_in not implemented yet")

    def get_current_stamp(self, stamp_type, signal_value, stamp):
        raise Exception("get_current_stamp not implemented yet")

    def create_relation_nodes(self, stamp_type, current_signal_value_node, signal_value, current_stamp):
        raise Exception("create_relation_nodes not implemented yet")

    def get_stamp_value(self, stamp):
        raise Exception("get_stamp_value not implemented yet")
