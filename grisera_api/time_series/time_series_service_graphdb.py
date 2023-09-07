from typing import Union, Optional

from starlette.datastructures import QueryParams

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from time_series.time_series_model import TimeSeriesPropertyIn, BasicTimeSeriesOut, \
    TimeSeriesNodesOut, TimeSeriesOut, TimeSeriesIn, TimeSeriesRelationIn
from models.not_found_model import NotFoundByIdModel
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

    def __init__(self):
        self.measure_service = None
        self.observable_information_service = None

    def save_time_series(self, time_series: TimeSeriesIn, dataset_name: str):
        """
        Send request to graph api to create new time series

        Args:
            time_series (TimeSeriesIn): Time series to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as time series object
        """
        node_response = self.graph_api_service.create_node("Time Series", dataset_name)

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

        Args:
            dataset_name (str): name of dataset
            params (QueryParams): Get parameters

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

    def get_time_series(self, time_series_id: Union[int, str], dataset_name: str, depth: int = 0,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None):
        """
        Send request to graph api to get given time series

        Args:
            time_series_id (int | str): identity of time series
            depth: (int): specifies how many related entities will be traversed to create the response
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value
            dataset_name (str): name of dataset

        Returns:
            Result of request as time series object
        """
        get_response = self.graph_api_service.get_node(time_series_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=time_series_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Time Series":
            return NotFoundByIdModel(id=time_series_id, errors="Node not found.")

        time_series = create_stub_from_response(get_response, properties=['type', 'source'])

        if depth != 0:
            time_series["observable_informations"] = []
            time_series["measure"] = None

            relations_response = self.graph_api_service.get_node_relationships(time_series_id, dataset_name)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == time_series_id & relation["name"] == "hasObservableInformation":
                    time_series["observable_informations"].append(self.observable_information_service.
                                                                  get_observable_information(relation["start_node"],
                                                                                             depth - 1))
                else:
                    if relation["start_node"] == time_series_id & relation["name"] == "hasMeasure":
                        time_series["measure"] = self.measure_service.get_measure(relation["start_node"],
                                                                                  depth - 1)
            return TimeSeriesOut(**time_series)
        else:
            return BasicTimeSeriesOut(**time_series)

    def delete_time_series(self, time_series_id: Union[int, str], dataset_name: str):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int | str): identity of time series
            dataset_name (str): name of dataset

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(time_series_id, dataset_name)
        return get_response

    def update_time_series(self, time_series_id: Union[int, str], time_series: TimeSeriesPropertyIn, dataset_name: str):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int | str): identity of time series
            time_series (TimeSeriesPropertyIn): Properties to update
            dataset_name (str): name of dataset

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(time_series_id, dataset_name)
        self.graph_api_service.create_properties(time_series_id, time_series, dataset_name)

        time_series_result = {"id": time_series_id, "type": get_response.type,
                              'signal_values': get_response.signal_values,
                              'source': get_response.source,
                              'additional_properties': get_response.additional_properties}
        time_series_result.update(time_series.dict())

        return BasicTimeSeriesOut(**time_series_result)

    def update_time_series_relationships(self, time_series_id: Union[int, str],
                                         time_series: TimeSeriesRelationIn, dataset_name: str):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int | str): identity of time series
            time_series (TimeSeriesRelationIn): Relationships to update
            dataset_name (str): name of dataset

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
                                                        end_node=time_series.measure_id,
                                                        name="hasMeasure",
                                                        dataset_name=dataset_name)
        return self.get_time_series(time_series_id, dataset_name)
