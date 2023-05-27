from typing import Union, Optional

from starlette.datastructures import QueryParams

from graph_api_service import GraphApiService
from mongo_service.mongo_api_service import MongoApiService
from helpers import create_stub_from_response
from time_series.time_series_model import (
    TimeSeriesPropertyIn,
    BasicTimeSeriesOut,
    TimeSeriesNodesOut,
    TimeSeriesOut,
    TimeSeriesIn,
    TimeSeriesRelationIn,
)
from models.not_found_model import NotFoundByIdModel
from time_series.time_series_service import TimeSeriesService


class TimeSeriesServiceMongoDB(TimeSeriesService):
    """
    Object to handle logic of time series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_service (MeasureService): Service to manage measure models
        observable_information_service (ObservableInformationService): Service to manage observable information models
    """

    def __init__(self):
        self.mongo_api_service = MongoApiService()
        self.model_out_class = TimeSeriesOut
        self.measure_service = None
        self.observable_information_service = None

    def save_time_series(self, time_series: TimeSeriesIn):
        """
        Send request to graph api to create new time series

        Args:
            time_series (TimeSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """

        related_oi = self.observable_information_service.get_observable_information(
            time_series.observable_information_id
        )
        related_oi_exists = related_oi is not NotFoundByIdModel
        if time_series.observable_information_id is not None and not related_oi_exists:
            return TimeSeriesOut(
                errors={"errors": "given observable information does not exist"}
            )

        # related_measure = self.measure_service.get_measure(time_series.measure_id)
        # related_measure_exists = related_measure is not NotFoundByIdModel
        # if time_series.measure_id is not None and not related_measure_exists:
        #     return TimeSeriesOut(errors={"errors": "given measure does not exist"})

        return self.mongo_api_service.create_time_series(time_series_in=time_series)

    def get_time_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """

    def get_time_series(
        self,
        time_series_id: Union[int, str],
        depth: int = 0,
        signal_min_value: Optional[int] = None,
        signal_max_value: Optional[int] = None,
    ):
        """
        Send request to graph api to get given time series

        Args:
            time_series_id (int | str): identity of time series
            depth: (int): specifies how many related entities will be traversed to create the response
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value

        Returns:
            Result of request as time series object
        """

    def delete_time_series(self, time_series_id: Union[int, str]):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int | str): identity of time series

        Returns:
            Result of request as time series object
        """

    def update_time_series(
        self, time_series_id: Union[int, str], time_series: TimeSeriesPropertyIn
    ):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int | str): identity of time series
            time_series (TimeSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """

    def update_time_series_relationships(
        self, time_series_id: Union[int, str], time_series: TimeSeriesRelationIn
    ):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int | str): identity of time series
            time_series (TimeSeriesRelationIn): Relationships to update

        Returns:
            Result of request as time series object
        """
