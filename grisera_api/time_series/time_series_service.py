from typing import Optional, List

from starlette.datastructures import QueryParams

from time_series.time_series_model import TimeSeriesPropertyIn, TimeSeriesIn, TimeSeriesRelationIn, \
    TimeSeriesTransformationIn


class TimeSeriesService:
    """
    Abstract class to handle logic of time series requests

    """

    def save_time_series(self, time_series: TimeSeriesIn):
        """
        Send request to graph api to create new time series

        Args:
            time_series (TimeSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """
        raise Exception("save_time_series not implemented yet")

    def transform_time_series(self, time_series_transformation: TimeSeriesTransformationIn):
        """
        Send request to graph api to create new transformed time series

        Args:
            time_series_transformation (TimeSeriesTransformationIn): Time series transformation parameters

        Returns:
            Result of request as time series object
        """
        raise Exception("transform_time_series not implemented yet")

    def get_time_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Args:
            params (QueryParams): Get parameters

        Returns:
            Result of request as list of time series nodes objects
        """
        raise Exception("get_time_series_nodes not implemented yet")

    def get_time_series(self, time_series_id: int,
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
        raise Exception("get_time_series not implemented yet")

    def get_time_series_multidimensional(self, time_series_ids: List[int]):
        """
        Send request to graph api to get given time series

        Args:
            time_series_ids (List[int]): Ids of the time series

        Returns:
            Result of request as time series object
        """
        raise Exception("get_time_series_multidimensional not implemented yet")

    def delete_time_series(self, time_series_id: int):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        raise Exception("delete_time_series not implemented yet")

    def update_time_series(self, time_series_id: int, time_series: TimeSeriesPropertyIn):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """
        raise Exception("update_time_series not implemented yet")

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
        raise Exception("update_time_series_relationships not implemented yet")
