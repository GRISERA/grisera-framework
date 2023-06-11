from typing import Union, Optional

from starlette.datastructures import QueryParams

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from signal_series.signal_series_model import SignalSeriesPropertyIn, BasicSignalSeriesOut, \
    SignalSeriesNodesOut, SignalSeriesOut, SignalSeriesIn, SignalSeriesRelationIn
from models.not_found_model import NotFoundByIdModel
from signal_series.signal_series_service import SignalSeriesService


class SignalSeriesServiceGraphDB(SignalSeriesService):
    """
    Object to handle logic of time series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_service (MeasureService): Service to manage measure models
        observable_information_service (ObservableInformationService): Service to manage observable information models
    """
    graph_api_service = GraphApiService()

    def __init__(self,signal_series_type_name):
        self.measure_service = None
        self.observable_information_service = None
        self.signal_series_type_name = signal_series_type_name


    def save_signal_series(self, signal_series: SignalSeriesIn):
        """
        Send request to graph api to create new time series

        Args:
            signal_series (SignalSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """
        node_response = self.graph_api_service.create_node(self.signal_series_type_name)

        if node_response["errors"] is not None:
            return SignalSeriesOut(**signal_series.dict(), errors=node_response["errors"])

        signal_series_id = node_response["id"]

        if signal_series.observable_information_id is not None and \
                type(self.observable_information_service.get_observable_information(
                    signal_series.observable_information_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=signal_series_id,
                                                        end_node=signal_series.observable_information_id,
                                                        name="hasObservableInformation")
        if signal_series.measure_id is not None and \
                type(self.measure_service.get_measure(signal_series.measure_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=signal_series_id,
                                                        end_node=signal_series.measure_id,
                                                        name="hasMeasure")

        signal_series.observable_information_id = signal_series.measure_id = None
        self.graph_api_service.create_properties(signal_series_id, signal_series)

        return self.get_signal_series(signal_series_id)

    def get_signal_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        get_response = self.graph_api_service.get_nodes("`"+self.signal_series_type_name+"`")

        signal_series_nodes = []

        for signal_series_node in get_response["nodes"]:
            properties = {'id': signal_series_node['id'], 'additional_properties': []}
            for property in signal_series_node["properties"]:
                if property["key"] in ["type", "source"]:
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            signal_series = BasicSignalSeriesOut(**properties)
            signal_series_nodes.append(signal_series)

        return SignalSeriesNodesOut(signal_series_nodes=signal_series_nodes)

    def get_signal_series(self, signal_series_id: Union[int, str], depth: int = 0,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None):
        """
        Send request to graph api to get given time series

        Args:
            signal_series_id (int | str): identity of time series
            depth: (int): specifies how many related entities will be traversed to create the response
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value

        Returns:
            Result of request as time series object
        """
        get_response = self.graph_api_service.get_node(signal_series_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=signal_series_id, errors=get_response["errors"])
        if get_response["labels"][0] != self.signal_series_type_name:
            return NotFoundByIdModel(id=signal_series_id, errors="Node not found.")

        signal_series = create_stub_from_response(get_response, properties=['type', 'source'])

        if depth != 0:
            signal_series["observable_informations"] = []
            signal_series["measure"] = None

            relations_response = self.graph_api_service.get_node_relationships(signal_series_id)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == signal_series_id & relation["name"] == "hasObservableInformation":
                    signal_series["observable_informations"].append(self.observable_information_service.
                                                                  get_observable_information(relation["start_node"],
                                                                                             depth - 1))
                else:
                    if relation["start_node"] == signal_series_id & relation["name"] == "hasMeasure":
                        signal_series["measure"] = self.measure_service.get_measure(relation["start_node"],
                                                                                  depth - 1)

            return SignalSeriesOut(**signal_series)
        else:
            return BasicSignalSeriesOut(**signal_series)

    def delete_signal_series(self, signal_series_id: Union[int, str]):
        """
        Send request to graph api to delete given time series

        Args:
            signal_series_id (int | str): identity of time series

        Returns:
            Result of request as time series object
        """
        get_response = self.get_signal_series(signal_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(signal_series_id)
        return get_response

    def update_signal_series(self, signal_series_id: Union[int, str], signal_series: SignalSeriesPropertyIn):
        """
        Send request to graph api to update given time series

        Args:
            signal_series_id (int | str): identity of time series
            signal_series (SignalSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """
        get_response = self.get_signal_series(signal_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(signal_series_id)
        self.graph_api_service.create_properties(signal_series_id, signal_series)

        signal_series_result = {"id": signal_series_id, "type": get_response.type,
                              'signal_values': get_response.signal_values,
                              'source': get_response.source,
                              'additional_properties': get_response.additional_properties}
        signal_series_result.update(signal_series.dict())

        return BasicSignalSeriesOut(**signal_series_result)

    def update_signal_series_relationships(self, signal_series_id: Union[int, str],
                                         signal_series: SignalSeriesRelationIn):
        """
        Send request to graph api to update given time series

        Args:
            signal_series_id (int | str): identity of time series
            signal_series (SignalSeriesRelationIn): Relationships to update

        Returns:
            Result of request as time series object
        """
        get_response = self.get_signal_series(signal_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if signal_series.observable_information_id is not None and \
                type(self.observable_information_service.get_observable_information(
                    signal_series.observable_information_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=signal_series_id,
                                                        end_node=signal_series.observable_information_id,
                                                        name="hasObservableInformation")
        if signal_series.measure_id is not None and \
                type(self.measure_service.get_measure(signal_series.measure_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=signal_series_id,
                                                        end_node=signal_series.measure_id,
                                                        name="hasMeasure")

        return self.get_signal_series(signal_series_id)