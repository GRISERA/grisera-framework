from typing import List, Optional

from starlette.datastructures import QueryParams

from models.not_found_model import NotFoundByIdModel
from time_series.helpers import get_node_property
from time_series.time_series_model import Type, TimeSeriesIn, TimeSeriesOut, SignalIn, SignalValueNodesIn, \
    TimestampNodesIn, TimeSeriesNodesOut, BasicTimeSeriesOut, TimeSeriesTransformationIn, \
    TimeSeriesTransformationRelationshipIn, TimeSeriesMultidimensionalOut
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from time_series.transformation.TimeSeriesTransformationFactory import TimeSeriesTransformationFactory
from time_series.transformation.multidimensional.TimeSeriesTransformationMultidimensional import \
    TimeSeriesTransformationMultidimensional


class TimeSeriesServiceGraphDBWithSignalValues(TimeSeriesServiceGraphDB):

    def save_time_series(self, time_series: TimeSeriesIn, dataset_name: str):
        """
        Send request to graph api to create new time series
        Args:
            time_series (TimeSeriesIn): Time series to be added
        Returns:
            Result of request as time series object
        """
        result = super().save_time_series(time_series, dataset_name)
        if result.errors is not None:
            return result

        time_series_id = result.id

        errors = self.save_signal_values(time_series.signal_values, time_series_id,
                                         self.get_experiment_id(time_series_id, dataset_name), time_series.type, dataset_name)
        if errors is not None:
            return TimeSeriesOut(**time_series.dict(), errors=errors)

        result.signal_values = self.get_signal_values(time_series_id, time_series.type, dataset_name)

        return result

    def transform_time_series(self, time_series_transformation: TimeSeriesTransformationIn, dataset_name):
        """
        Send request to graph api to create new transformed time series

        Args:
            time_series_transformation (TimeSeriesTransformationIn): Time series transformation parameters

        Returns:
            Result of request as time series object
        """
        source_time_series = []
        for time_series_id in time_series_transformation.source_time_series_ids:
            time_series = self.get_time_series(time_series_id, dataset_name)
            if time_series.errors is not None:
                return time_series
            source_time_series.append(time_series)
        try:
            new_time_series, new_signal_values_id_mapping = TimeSeriesTransformationFactory().get_transformation(
                time_series_transformation.name) \
                .transform(source_time_series, time_series_transformation.additional_properties)
        except Exception as e:
            return TimeSeriesNodesOut(errors=str(e))
        new_time_series.measure_id = time_series_transformation.destination_measure_id
        new_time_series.observable_information_id = time_series_transformation.destination_observable_information_id

        result = self.save_time_series(new_time_series, dataset_name)

        for index, time_series_id in enumerate(time_series_transformation.source_time_series_ids):
            relationship = self.graph_api_service.create_relationships(result.id, time_series_id, "transformedFrom", dataset_name)
            self.graph_api_service.create_relationship_properties(relationship["id"],
                                                                  TimeSeriesTransformationRelationshipIn(
                                                                      additional_properties=[

                                                                          {'key': 'order', 'value': index + 1}]))
        assert len(new_signal_values_id_mapping) == len(
            result.signal_values), "transformation signal values mapping does not have correct length"
        for signal_value_ids, new_signal_value in zip(new_signal_values_id_mapping, result.signal_values):
            new_signal_value_id = new_signal_value["signal_value"]["id"]
            for index, old_signal_value_id in enumerate(signal_value_ids):
                relationship = self.graph_api_service.create_relationships(new_signal_value_id, old_signal_value_id,
                                                                           "basedOn", dataset_name)
                self.graph_api_service.create_relationship_properties(relationship["id"],
                                                                      TimeSeriesTransformationRelationshipIn(
                                                                          additional_properties=[
                                                                              {'key': 'order', 'value': index + 1}]), dataset_name)
        return result

    def get_experiment_id(self, time_series_id: int, dataset_name: str):
        query = {
            "nodes": [
                {
                    "id": time_series_id,
                    "label": "Time Series"
                },
                {
                    "label": "Observable Information"
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
        response = self.graph_api_service.get_nodes_by_query(query, dataset_name)
        for row in response["rows"]:
            return row[0]["id"]
        return None

    def get_neighbour_node_id(self, node_id: int, relation_name: str, dataset_name: str, forward: bool = True):
        relations_response = self.graph_api_service.get_node_relationships(node_id, dataset_name)
        for relation in relations_response["relationships"]:
            if relation["name"] == relation_name:
                if relation["start_node" if forward else "end_node"] == node_id:
                    return relation["end_node" if forward else "start_node"], relation["id"]
        return None, None

    def get_neighbour_node(self, node_id: int, relation_name: str, dataset_name: str, forward: bool = True):
        neighbour_node_id, relation_id = self.get_neighbour_node_id(node_id, relation_name, dataset_name, forward)
        if neighbour_node_id is not None:
            get_response = self.graph_api_service.get_node(neighbour_node_id, dataset_name)
            if get_response["errors"] is None:
                return get_response, relation_id
        return None, None


    def get_or_create_timestamp_node(self, timestamp_value: int, timestamp, dataset_name: str):
        if timestamp_value is None:
            return {"errors": "Timestamp value is None. Please check time series type."}
        previous_timestamp_id = None
        previous_timestamp_timestamp_relation_id = None
        while timestamp is not None and int(get_node_property(timestamp, "timestamp")) < timestamp_value:
            previous_timestamp_id = timestamp["id"]
            timestamp, previous_timestamp_timestamp_relation_id = self.get_neighbour_node(timestamp["id"], "next", dataset_name)

        if timestamp is None or int(get_node_property(timestamp, "timestamp")) != timestamp_value:
            new_timestamp_node = self.graph_api_service.create_node("`Timestamp`", dataset_name)

            if new_timestamp_node["errors"] is not None:
                return new_timestamp_node

            new_timestamp_id = new_timestamp_node["id"]

            timestamp_properties_response = self.graph_api_service.create_properties(new_timestamp_id,
                                                                                     TimestampNodesIn(
                                                                                         timestamp=timestamp_value), dataset_name)
            if timestamp_properties_response["errors"] is not None:
                return timestamp_properties_response

            if previous_timestamp_id is not None:
                self.graph_api_service.create_relationships(start_node=previous_timestamp_id,
                                                            end_node=new_timestamp_id,
                                                            name="next")
            if timestamp is not None:
                self.graph_api_service.create_relationships(start_node=new_timestamp_id,
                                                            end_node=timestamp["id"],
                                                            name="next")
            if previous_timestamp_timestamp_relation_id is not None:
                self.graph_api_service.delete_relationship(previous_timestamp_timestamp_relation_id, dataset_name)

            return self.graph_api_service.get_node(new_timestamp_id, dataset_name)
        return timestamp


    def create_signal_value(self, signal_value: SignalValueNodesIn, previous_signal_value_node, time_series_id: int):
        signal_value_node_response = self.graph_api_service.create_node("`Signal Value`")

        if signal_value_node_response["errors"] is not None:
            return signal_value_node_response

        signal_value_properties_response = self.graph_api_service.create_properties(signal_value_node_response["id"],
                                                                                    signal_value)
        if signal_value_properties_response["errors"] is not None:
            return signal_value_properties_response

        if previous_signal_value_node is None:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=signal_value_node_response["id"],
                                                        name="hasSignal")
        else:
            self.graph_api_service.create_relationships(start_node=previous_signal_value_node["id"],
                                                        end_node=signal_value_node_response["id"],
                                                        name="next")

        return signal_value_node_response

    def save_signal_values(self, signal_values: List[SignalIn], time_series_id: int, experiment_id: int,
                           timestamp_type: Type, dataset_name: str):

        timestamp, experiment_timestamp_relation_id = self.get_neighbour_node(experiment_id, "takes", dataset_name) \
            if experiment_id is not None else (None, None)
        signal_value_node = None

        for signal_value in signal_values:
            current_signal_value_node = self.create_signal_value(signal_value.signal_value, signal_value_node,
                                                                 time_series_id)

            if current_signal_value_node["errors"] is not None:
                return current_signal_value_node

            current_timestamp = self.get_or_create_timestamp_node(
                signal_value.timestamp if timestamp_type == Type.timestamp else signal_value.start_timestamp, timestamp, dataset_name)

            if current_timestamp["errors"] is not None:
                return current_timestamp["errors"]

            if signal_value_node is None and (
                    timestamp is None or int(get_node_property(current_timestamp, "timestamp")) < int(
                    get_node_property(timestamp, "timestamp"))):
                if experiment_timestamp_relation_id is not None:
                    self.graph_api_service.delete_relationship(experiment_timestamp_relation_id, dataset_name)
                if experiment_id is not None:
                    self.graph_api_service.create_relationships(start_node=experiment_id,
                                                                end_node=current_timestamp["id"],
                                                                name="takes")

            if timestamp_type == Type.timestamp:
                self.graph_api_service.create_relationships(start_node=current_timestamp["id"],
                                                            end_node=current_signal_value_node["id"],
                                                            name="inSec")
            else:
                self.graph_api_service.create_relationships(start_node=current_timestamp["id"],
                                                            end_node=current_signal_value_node["id"],
                                                            name="startInSec")
                current_timestamp = self.get_or_create_timestamp_node(signal_value.end_timestamp, current_timestamp, dataset_name)

                if current_timestamp["errors"] is not None:
                    return current_timestamp["errors"]

                self.graph_api_service.create_relationships(start_node=current_timestamp["id"],
                                                            end_node=current_signal_value_node["id"],
                                                            name="endInSec")

            timestamp = current_timestamp
            signal_value_node = current_signal_value_node
        return None

    def get_time_series(self, time_series_id: int, dataset_name: str,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None):
        """
        Send request to graph api to get given time series
        Args:
            time_series_id (int): Id of time series
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value
        Returns:
            Result of request as time series object
        """
        time_series = super().get_time_series(time_series_id, dataset_name)
        if time_series.errors is None:
            time_series.signal_values = self.get_signal_values(time_series_id, time_series.type,
                                                               signal_min_value, signal_max_value)
        return time_series

    def get_time_series_multidimensional(self, time_series_ids: List[int]):
        """
        Send request to graph api to get given time series
        Args:
            time_series_ids (TimeSeriesIds): Ids of the time series
        Returns:
            Result of request as time series object
        """
        source_time_series = []
        for time_series_id in time_series_ids:
            time_series = self.get_time_series(time_series_id)
            if time_series.errors is not None:
                return time_series
            source_time_series.append(time_series)
        try:
            result = TimeSeriesTransformationMultidimensional().transform(source_time_series)
            for time_series in source_time_series:
                time_series.signal_values = []
            result.time_series = source_time_series
            return result
        except Exception as e:
            return TimeSeriesMultidimensionalOut(errors=str(e))

    def get_signal_values(self, time_series_id: int, time_series_type: str,
                          signal_min_value: Optional[int] = None,
                          signal_max_value: Optional[int] = None):
        """
        Send requests to graph api to get all signal values
        Args:
            time_series_id (int): id of the time series
            time_series_type (str): type of the time series
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value
        Returns:
            Array of signal value objects
        """

        parameters = []
        if signal_min_value is not None:
            parameters.append({
                "key": "value",
                "operator": "greater",
                "value": signal_min_value
            })
        if signal_max_value is not None:
            parameters.append({
                "key": "value",
                "operator": "less",
                "value": signal_max_value
            })
        query_timestamp = {
            "nodes": [
                {
                    "id": time_series_id,
                    "label": "Time Series"
                },
                {
                    "label": "Signal Value"
                },
                {
                    "label": "Signal Value",
                    "result": True,
                    "parameters": parameters
                },
                {
                    "label": "Timestamp",
                    "result": True
                }
            ],
            "relations": [
                {
                    "begin_node_index": 0,
                    "end_node_index": 1,
                    "label": "hasSignal"
                },
                {
                    "begin_node_index": 1,
                    "end_node_index": 2,
                    "label": "next",
                    "min_count": 0
                },
                {
                    "begin_node_index": 3,
                    "end_node_index": 2,
                    "label": "inSec"
                }
            ]
        }
        query_epoch = {
            "nodes": [
                {
                    "id": time_series_id,
                    "label": "Time Series"
                },
                {
                    "label": "Signal Value"
                },
                {
                    "label": "Signal Value",
                    "result": True,
                    "parameters": parameters
                },
                {
                    "label": "Timestamp",
                    "result": True
                },
                {
                    "label": "Timestamp",
                    "result": True
                }
            ],
            "relations": [
                {
                    "begin_node_index": 0,
                    "end_node_index": 1,
                    "label": "hasSignal"
                },
                {
                    "begin_node_index": 1,
                    "end_node_index": 2,
                    "label": "next",
                    "min_count": 0
                },
                {
                    "begin_node_index": 3,
                    "end_node_index": 2,
                    "label": "startInSec"
                },
                {
                    "begin_node_index": 4,
                    "end_node_index": 2,
                    "label": "endInSec"
                }
            ]
        }
        response = self.graph_api_service.get_nodes_by_query(
            query_timestamp if time_series_type == Type.timestamp.value else query_epoch)
        signal_values = []
        for row in response["rows"]:
            if time_series_type == Type.timestamp:
                signal_values.append({'signal_value': row[0], 'timestamp': row[1]})
            else:
                signal_values.append({'signal_value': row[0], 'start_timestamp': row[1], 'end_timestamp': row[2]})
        return signal_values

    def get_time_series_nodes(self, params: QueryParams, dataset_name):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        query = {
            "nodes": [
                {
                    "label": "Time Series",
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
            if label == "Observable Information":
                query["relations"].append({
                    "begin_node_index": 0,
                    "end_node_index": new_node_index,
                    "label": "hasObservableInformation"
                })
            elif label == "Recording":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Observable Information"),
                    "end_node_index": new_node_index,
                    "label": "hasRecording"
                })
            elif label == "Participation":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Recording"),
                    "end_node_index": new_node_index,
                    "label": "hasParticipation"
                })
            elif label == "Participant State":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Participation"),
                    "end_node_index": new_node_index,
                    "label": "hasParticipantState"
                })
            elif label == "Participant":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Participant State"),
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
            elif label == "Registered Channel":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Recording"),
                    "end_node_index": new_node_index,
                    "label": "hasRegisteredChannel"
                })
            elif label == "Channel":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Registered Channel"),
                    "end_node_index": new_node_index,
                    "label": "hasChannel"
                })
            elif label == "Registered Data":
                query["relations"].append({
                    "begin_node_index": get_or_append_node_to_query(query, node_indexes, "Channel"),
                    "end_node_index": new_node_index,
                    "label": "hasRegisteredData"
                })
            else:
                print("Unknown node label")
            return new_node_index

        node_indexes = {}
        for node_label in ["Observable Information", "Recording", "Participation", "Participant State", "Participant",
                           "Activity Execution", "Activity", "Experiment", "Registered Channel", "Channel",
                           "Registered Data"]:
            node_param_name = node_label.lower().replace(" ", "")
            if node_param_name in params_per_node:
                node_id = None
                if "id" in params_per_node[node_param_name]:
                    node_id = int(params_per_node[node_param_name]["id"])
                    del params_per_node[node_param_name]["id"]
                get_or_append_node_to_query(query, node_indexes, node_label, node_id, params_per_node[node_param_name])

        response = self.graph_api_service.get_nodes_by_query(query, dataset_name)

        time_series_nodes = []
        for time_series_row in response["rows"]:
            time_series_node = time_series_row[0]
            properties = {'id': time_series_node['id'], 'additional_properties': []}
            for property in time_series_node["properties"]:
                if property["key"] in ["type", "source"]:
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            time_series = BasicTimeSeriesOut(**properties)
            time_series_nodes.append(time_series)

        return TimeSeriesNodesOut(time_series_nodes=time_series_nodes)

    def delete_time_series(self, time_series_id: int, dataset_name: str):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        get_response = super().delete_time_series(time_series_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        timestamp_ids_to_analyze = []
        for signal_value in get_response.signal_values:
            self.graph_api_service.delete_node(signal_value["signal_value"]["id"], dataset_name)
            if get_response.type == Type.timestamp.value:
                timestamp_ids_to_analyze.append(signal_value["timestamp"]["id"])
            else:
                timestamp_ids_to_analyze.append(signal_value["start_timestamp"]["id"])
                timestamp_ids_to_analyze.append(signal_value["end_timestamp"]["id"])
        for timestamp_id in timestamp_ids_to_analyze:
            neighbour_signal_a_id, _ = self.get_neighbour_node_id(timestamp_id, "inSec", dataset_name)
            neighbour_signal_b_id, _ = self.get_neighbour_node_id(timestamp_id, "startInSec", dataset_name)
            neighbour_signal_c_id, _ = self.get_neighbour_node_id(timestamp_id, "endInSec", dataset_name)
            if neighbour_signal_a_id is None and neighbour_signal_b_id is None and neighbour_signal_c_id is None:
                next_timestamp_id, _ = self.get_neighbour_node_id(timestamp_id, "next", dataset_name)
                previous_timestamp_id, _ = self.get_neighbour_node_id(timestamp_id, "next", dataset_name, False)
                previous_experiment_id, _ = self.get_neighbour_node_id(timestamp_id, "takes", dataset_name, False)

                self.graph_api_service.delete_node(timestamp_id, dataset_name)

                if next_timestamp_id is not None:
                    if previous_experiment_id is not None:
                        self.graph_api_service.create_relationships(start_node=previous_experiment_id,
                                                                    end_node=next_timestamp_id,
                                                                    name="takes", dataset_name=dataset_name)
                    elif previous_timestamp_id is not None:
                        self.graph_api_service.create_relationships(start_node=previous_timestamp_id,
                                                                    end_node=next_timestamp_id,
                                                                    name="next", dataset_name=dataset_name)
        return get_response
