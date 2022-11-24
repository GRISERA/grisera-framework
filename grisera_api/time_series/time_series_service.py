from typing import List

from graph_api_service import GraphApiService
from measure.measure_service import MeasureService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from observable_information.observable_information_service import ObservableInformationService
from time_series.time_series_model import TimeSeriesPropertyIn, BasicTimeSeriesOut, \
    TimeSeriesNodesOut, TimeSeriesOut, TimeSeriesIn, TimeSeriesRelationIn, SignalValueNodesIn, TimestampNodesIn, \
    SignalIn


class TimeSeriesService:
    """
    Object to handle logic of time series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_service (MeasureService): Service to manage measure models
        observable_information_service (ObservableInformationService): Service to manage observable information models
    """
    graph_api_service = GraphApiService()
    measure_service = MeasureService()
    observable_information_service = ObservableInformationService()

    def save_time_series(self, time_series: TimeSeriesIn):
        """
        Send request to graph api to create new time series

        Args:
            time_series (TimeSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """
        node_response = self.graph_api_service.create_node("`Time Series`")

        if node_response["errors"] is not None:
            return TimeSeriesOut(**time_series.dict(), errors=node_response["errors"])

        time_series_id = node_response["id"]

        if time_series.observable_information_id is not None and \
                type(self.observable_information_service.get_observable_information(
                    time_series.observable_information_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.observable_information_id,
                                                        name="hasObservableInformation")
        if time_series.measure_id is not None and \
                type(self.measure_service.get_measure(time_series.measure_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.measure_id,
                                                        name="hasMeasure")

        time_series.observable_information_id = time_series.measure_id = None
        self.graph_api_service.create_properties(time_series_id, time_series)

        errors = self.save_signal_values(time_series.signal_values, time_series_id, 53)
        if errors is not None:
            return TimeSeriesOut(**time_series.dict(), errors=errors)

        return self.get_time_series(time_series_id)

    def get_neighbour_node_id(self, node_id: int, relation_name: str, forward: bool = True):
        relations_response = self.graph_api_service.get_node_relationships(node_id)
        for relation in relations_response["relationships"]:
            if relation["name"] == relation_name:
                if relation["start_node" if forward else "end_node"] == node_id:
                    return relation["end_node" if forward else "start_node"], relation["id"]
        return None, None

    def get_neighbour_node(self, node_id: int, relation_name: str, forward: bool = True):
        neighbour_node_id, relation_id = self.get_neighbour_node_id(node_id, relation_name, forward)
        if neighbour_node_id is not None:
            get_response = self.graph_api_service.get_node(neighbour_node_id)
            if get_response["errors"] is None:
                return get_response, relation_id
        return None, None

    def get_node_property(self, node, property_key: str):
        if node is not None:
            for node_property in node["properties"]:
                if node_property["key"] == property_key:
                    return node_property["value"]
        return None

    def save_signal_values(self, signal_values: List[SignalIn], time_series_id: int, experiment_id: int):
        previous_signal_value_id = None

        timestamp, experiment_timestamp_relation_id = self.get_neighbour_node(experiment_id, "takes")
        previous_timestamp_id = None
        previous_timestamp_timestamp_relation_id = None

        for signal_value in signal_values:
            while timestamp is not None and int(
                    self.get_node_property(timestamp, "timestamp")) < signal_value.timestamp:
                previous_timestamp_id = timestamp["id"]
                experiment_timestamp_relation_id = None
                timestamp, previous_timestamp_timestamp_relation_id = self.get_neighbour_node(timestamp["id"], "next")

            if timestamp is None or int(self.get_node_property(timestamp, "timestamp")) != signal_value.timestamp:
                timestamp_node_response = self.graph_api_service.create_node("`Timestamp`")

                if timestamp_node_response["errors"] is not None:
                    return timestamp_node_response["errors"]

                new_timestamp_id = timestamp_node_response["id"]

                timestamp_properties_response = self.graph_api_service.create_properties(new_timestamp_id,
                                                                                         TimestampNodesIn(
                                                                                             timestamp=signal_value.timestamp))
                if timestamp_properties_response["errors"] is not None:
                    return timestamp_properties_response["errors"]

                if previous_timestamp_id is None:
                    self.graph_api_service.create_relationships(start_node=experiment_id,
                                                                end_node=new_timestamp_id,
                                                                name="takes")
                else:
                    self.graph_api_service.create_relationships(start_node=previous_timestamp_id,
                                                                end_node=new_timestamp_id,
                                                                name="next")
                if timestamp is not None:
                    self.graph_api_service.create_relationships(start_node=new_timestamp_id,
                                                                end_node=timestamp["id"],
                                                                name="next")
                if previous_timestamp_timestamp_relation_id is not None:
                    self.graph_api_service.delete_relationship(previous_timestamp_timestamp_relation_id)
                elif experiment_timestamp_relation_id is not None:
                    self.graph_api_service.delete_relationship(experiment_timestamp_relation_id)

                timestamp = self.graph_api_service.get_node(new_timestamp_id)

            signal_value_node_response = self.graph_api_service.create_node("`Signal Value`")

            if signal_value_node_response["errors"] is not None:
                return signal_value_node_response["errors"]

            signal_value_id = signal_value_node_response["id"]

            signal_value_properties_response = self.graph_api_service.create_properties(signal_value_id,
                                                                                        SignalValueNodesIn(
                                                                                            value=signal_value.value))
            if signal_value_properties_response["errors"] is not None:
                return signal_value_properties_response["errors"]

            if previous_signal_value_id is None:
                self.graph_api_service.create_relationships(start_node=time_series_id,
                                                            end_node=signal_value_id,
                                                            name="hasSignal")
            else:
                self.graph_api_service.create_relationships(start_node=previous_signal_value_id,
                                                            end_node=signal_value_id,
                                                            name="next")
            self.graph_api_service.create_relationships(start_node=signal_value_id,
                                                        end_node=timestamp["id"],
                                                        name="inSec")

            previous_signal_value_id = signal_value_id
        return None

    def get_time_series_nodes(self):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        get_response = self.graph_api_service.get_nodes("`Time Series`")

        time_series_nodes = []

        for time_series_node in get_response["nodes"]:
            properties = {'id': time_series_node['id'], 'additional_properties': []}
            for property in time_series_node["properties"]:
                if property["key"] in ["type", "source"]:
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            time_series = BasicTimeSeriesOut(**properties)
            time_series_nodes.append(time_series)

        return TimeSeriesNodesOut(time_series_nodes=time_series_nodes)

    def get_time_series(self, time_series_id: int):
        """
        Send request to graph api to get given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        get_response = self.graph_api_service.get_node(time_series_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=time_series_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Time Series":
            return NotFoundByIdModel(id=time_series_id, errors="Node not found.")

        time_series = {'id': get_response['id'], 'additional_properties': [], 'relations': [],
                       'reversed_relations': [], 'signal_values': []}
        for property in get_response["properties"]:
            if property["key"] in ["type", "source"]:
                time_series[property["key"]] = property["value"]
            else:
                time_series['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(time_series_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == time_series_id:
                time_series['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                    name=relation["name"],
                                                                    relation_id=relation["id"]))
                if relation["name"] == "hasSignal":
                    time_series['signal_values'] = self.get_signal_values(relation["end_node"])
            else:
                time_series['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                             name=relation["name"],
                                                                             relation_id=relation["id"]))

        return TimeSeriesOut(**time_series)

    def get_signal_values(self, first_signal_value_id: int):
        """
        Send requests to graph api to get all signal values

        Args:
            first_signal_value_id (int): Id of the first signal value

        Returns:
            Array of signal value objects
        """
        signal_values = []
        current_signal_node_id = first_signal_value_id
        while current_signal_node_id is not None:
            signal_value_get_response = self.graph_api_service.get_node(current_signal_node_id)

            if signal_value_get_response["errors"] is not None:
                return NotFoundByIdModel(id=current_signal_node_id, errors=signal_value_get_response["errors"])

            signal_value_node_relations_response = self.graph_api_service.get_node_relationships(current_signal_node_id)

            next_signal_node_id = None
            for signal_value_node_relation in signal_value_node_relations_response["relationships"]:
                if signal_value_node_relation["start_node"] == current_signal_node_id:
                    if signal_value_node_relation["name"] == "next":
                        next_signal_node_id = signal_value_node_relation["end_node"]
                    if signal_value_node_relation["name"] == "inSec":
                        timestamp_get_response = self.graph_api_service.get_node(signal_value_node_relation["end_node"])

                        if timestamp_get_response["errors"] is not None:
                            return NotFoundByIdModel(id=signal_value_node_relation["end_node"],
                                                     errors=timestamp_get_response["errors"])
                        signal_values.append({'id': signal_value_get_response['id'],
                                              'properties': signal_value_get_response['properties'],
                                              'timestamp': timestamp_get_response['properties']})
            current_signal_node_id = next_signal_node_id
        return signal_values

    def delete_time_series(self, time_series_id: int):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(time_series_id)
        return get_response

    def update_time_series(self, time_series_id: int, time_series: TimeSeriesPropertyIn):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(time_series_id)
        self.graph_api_service.create_properties(time_series_id, time_series)

        time_series_result = {"id": time_series_id, "relations": get_response.relations,
                                    "reversed_relations": get_response.reversed_relations}
        time_series_result.update(time_series.dict())

        return TimeSeriesOut(**time_series_result)

    def update_time_series_relationships(self, time_series_id: int,
                                               time_series: TimeSeriesRelationIn):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesRelationIn): Relationships to update

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if time_series.observable_information_id is not None and \
                type(self.observable_information_service.get_observable_information(
                    time_series.observable_information_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.observable_information_id,
                                                        name="hasObservableInformation")
        if time_series.measure_id is not None and \
                type(self.measure_service.get_measure(time_series.measure_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.personality_id,
                                                        name="hasMeasure")

        return self.get_time_series(time_series_id)
