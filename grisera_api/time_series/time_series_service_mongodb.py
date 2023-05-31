from typing import Union, Optional

from starlette.datastructures import QueryParams

from graph_api_service import GraphApiService
from mongo_service.collection_mapping import Collections
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

        created_ts_id = self.mongo_api_service.create_time_series(
            time_series_in=time_series
        )
        return self.get_time_series(created_ts_id)

    def get_multiple(self, query: dict = {}, depth: int = 0, source: str = ""):
        results_dict = self.mongo_api_service.get_many_time_series(query)

        for result in results_dict:
            self._add_related_documents(result, depth, source)

        return results_dict

    def get_time_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        time_series_dicts = self.get_multiple()
        results = [BasicTimeSeriesOut(**ts_dict) for ts_dict in time_series_dicts]
        return TimeSeriesNodesOut(time_series_nodes=results)

    def get_time_series(
        self,
        time_series_id: Union[int, str],
        depth: int = 0,
        signal_min_value: Optional[int] = None,
        signal_max_value: Optional[int] = None,
        source: str = "",
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
        time_series = self.mongo_api_service.get_time_series(
            ts_id=time_series_id,
            signal_min_value=signal_min_value,
            signal_max_value=signal_max_value,
        )
        self._add_related_documents(time_series, depth, source)
        return time_series

    def delete_time_series(self, time_series_id: Union[int, str]):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int | str): identity of time series

        Returns:
            Result of request as time series object
        """
        get_response = self.get_time_series(time_series_id)
        self.mongo_api_service.delete_time_series(time_series_id)
        return get_response

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
        time_series.signal_values = []
        update_dict = time_series.dict()
        update_dict.pop("signal_values")
        self.mongo_api_service.update_time_series_metadata(update_dict, time_series_id)
        return self.get_time_series(time_series_id)

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
        get_response = self.get_time_series(time_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

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

        self.mongo_api_service.update_time_series_metadata(
            time_series.dict(), time_series_id
        )
        return self.get_time_series(time_series_id)

    def get_time_series_for_observable_information(
        self,
        observable_information_id: Union[str, int],
        depth: int = 0,
        source: str = "",
    ):
        query = {"metadata.observable_information_id": observable_information_id}
        return self.get_multiple(query, depth, source)

    def _add_related_documents(self, time_series: dict, depth: int, source: str):
        if depth > 0:
            self._add_mesure(time_series, depth, source)
            self._add_observable_informations(time_series, depth, source)

    def _add_mesure(self, time_series: dict, depth: int, source: str):
        pass

    def _add_observable_informations(self, time_series: dict, depth: int, source: str):
        has_related_oi = time_series["observable_information_id"] is not None
        if source != Collections.OBSERVABLE_INFORMATION and has_related_oi:
            time_series["observable_informations"] = [
                self.observable_information_service.get_single_dict(
                    time_series["observable_information_id"],
                    depth=depth - 1,
                    source=Collections.TIME_SERIES,
                )
            ]
