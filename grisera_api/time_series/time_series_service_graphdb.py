from typing import Optional

from starlette.datastructures import QueryParams

from graph_api_service import GraphApiService
from measure.measure_service_graphdb import MeasureServiceGraphDB
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB
from time_series.time_series_model import TimeSeriesPropertyIn, BasicTimeSeriesOut, \
    TimeSeriesNodesOut, TimeSeriesOut, TimeSeriesIn, TimeSeriesRelationIn
from time_series.time_series_service import TimeSeriesService


class TimeSeriesServiceGraphDB(TimeSeriesService):
    """
    Object to handle logic of time series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_service (MeasureService): Service to manage measure models
        observable_information_service (ObservableInformationService): Service to manage observable information models
    """
    graph_api_service = GraphApiService()
    measure_service = MeasureServiceGraphDB()
    observable_information_service = ObservableInformationServiceGraphDB()

    def save_time_series(self, time_series: TimeSeriesIn, dataset_name: str):
        """
        Send request to graph api to create new time series

        Args:
            time_series (TimeSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """
        node_response = self.graph_api_service.create_node("`Time Series`", dataset_name)

        if node_response["errors"] is not None:
            return TimeSeriesOut(**time_series.dict(), errors=node_response["errors"])

        time_series_id = node_response["id"]

        if time_series.observable_information_id is not None and \
                type(self.observable_information_service.get_observable_information(
                    time_series.observable_information_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.observable_information_id,
                                                        name="hasObservableInformation",
                                                        dataset_name=dataset_name)
        if time_series.measure_id is not None and \
                type(self.measure_service.get_measure(time_series.measure_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.measure_id,
                                                        name="hasMeasure",
                                                        dataset_name=dataset_name)

        time_series.observable_information_id = time_series.measure_id = None
        self.graph_api_service.create_properties(time_series_id, time_series, dataset_name)

        return self.get_time_series(time_series_id, dataset_name)

    def get_time_series_nodes(self, dataset_name: str, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        get_response = self.graph_api_service.get_nodes("`Time Series`", dataset_name)

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
        get_response = self.graph_api_service.get_node(time_series_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=time_series_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Time Series":
            return NotFoundByIdModel(id=time_series_id, errors="Node not found.")

        time_series = {'id': get_response['id'], 'additional_properties': [], 'relations': [],
                             'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] in ["type", "source"]:
                time_series[property["key"]] = property["value"]
            else:
                time_series['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(time_series_id, dataset_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == time_series_id:
                time_series['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                          name=relation["name"],
                                                                          relation_id=relation["id"]))
            else:
                time_series['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                                   name=relation["name"],
                                                                                   relation_id=relation["id"]))

        return TimeSeriesOut(**time_series)

    def delete_time_series(self, time_series_id: int, dataset_name: str):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(time_series_id, dataset_name)
        return get_response

    def update_time_series(self, time_series_id: int, time_series: TimeSeriesPropertyIn, dataset_name: str):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(time_series_id, dataset_name)
        self.graph_api_service.create_properties(time_series_id, time_series, dataset_name)

        time_series_result = {"id": time_series_id, "relations": get_response.relations,
                                    "reversed_relations": get_response.reversed_relations}
        time_series_result.update(time_series.dict())

        return TimeSeriesOut(**time_series_result)

    def update_time_series_relationships(self, time_series_id: int,
                                               time_series: TimeSeriesRelationIn, dataset_name: str):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesRelationIn): Relationships to update

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if time_series.observable_information_id is not None and \
                type(self.observable_information_service.get_observable_information(
                    time_series.observable_information_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.observable_information_id,
                                                        name="hasObservableInformation",
                                                        dataset_name=dataset_name)
        if time_series.measure_id is not None and \
                type(self.measure_service.get_measure(time_series.measure_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=time_series_id,
                                                        end_node=time_series.personality_id,
                                                        name="hasMeasure",
                                                        dataset_name=dataset_name)

        return self.get_time_series(time_series_id, dataset_name)
