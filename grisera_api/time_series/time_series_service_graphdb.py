from typing import Union, Optional

from starlette.datastructures import QueryParams

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from signal_series.signal_series_model import SignalSeriesPropertyIn, BasicSignalSeriesOut, \
    SignalSeriesNodesOut, SignalSeriesOut, SignalSeriesIn, SignalSeriesRelationIn
from models.not_found_model import NotFoundByIdModel
from signal_series.signal_series_service_graphdb import SignalSeriesServiceGraphDB


class TimeSeriesServiceGraphDB(SignalSeriesServiceGraphDB):
    """
    Object to handle logic of time series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_service (MeasureService): Service to manage measure models
        observable_information_service (ObservableInformationService): Service to manage observable information models
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        super().__init__("Time_Series")

    def save_signal_series(self, signal_series: SignalSeriesIn):
        """
        Send request to graph api to create new time series

        Args:
            signal_series (SignalSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """
        return super().save_signal_series(signal_series)

    def get_signal_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        return super().get_signal_series_nodes(params)

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
        return super().get_signal_series(signal_series_id,depth, signal_min_value, signal_max_value)

    def delete_signal_series(self, signal_series_id: Union[int, str]):
        """
        Send request to graph api to delete given time series

        Args:
            signal_series_id (int | str): identity of time series

        Returns:
            Result of request as time series object
        """
        return super().delete_signal_series(signal_series_id)

    def update_signal_series(self, signal_series_id: Union[int, str], signal_series: SignalSeriesPropertyIn):
        """
        Send request to graph api to update given time series

        Args:
            signal_series_id (int | str): identity of time series
            signal_series (SignalSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """
        return super().update_signal_series(signal_series_id, signal_series)

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
        return super().update_signal_series_relationships(signal_series_id, signal_series)
