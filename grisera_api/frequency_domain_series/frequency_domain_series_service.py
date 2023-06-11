from typing import Union, Optional, List

from starlette.datastructures import QueryParams
from signal_series.signal_series_service import SignalSeriesService

from signal_series.signal_series_model import SignalSeriesPropertyIn, SignalSeriesIn, SignalSeriesRelationIn, \
    SignalSeriesTransformationIn


class TimeSeriesService(SignalSeriesService):
    """
    Abstract class to handle logic of signal series requests

    """

    def save_signal_series(self, signal_series: SignalSeriesIn):
        """
        Send request to graph api to create new signal series

        Args:
            signal_series (SignalSeriesIn): signal series to be added

        Returns:
            Result of request as signal series object
        """
        raise Exception("save_signal_series not implemented yet")

    def transform_signal_series(self, signal_series_transformation: SignalSeriesTransformationIn):
        """
        Send request to graph api to create new transformed signal series

        Args:
            signal_series_transformation (SignalSeriesTransformationIn): signal series transformation parameters

        Returns:
            Result of request as signal series object
        """
        raise Exception("transform_signal_series not implemented yet")

    def get_signal_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get signal series nodes

        Args:
            params (QueryParams): Get parameters

        Returns:
            Result of request as list of signal series nodes objects
        """
        raise Exception("get_signal_series_nodes not implemented yet")

    def get_signal_series(self, signal_series_id: Union[int, str], depth: int = 0,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None):
        """
        Send request to graph api to get given signal series

        Args:
            signal_series_id (int | str): identity of signal series
            depth: (int): specifies how many related entities will be traversed to create the response
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value

        Returns:
            Result of request as signal series object
        """
        raise Exception("get_signal_series not implemented yet")

    def get_signal_series_multidimensional(self, signal_series_ids: List[Union[int, str]]):
        """
        Send request to graph api to get given signal series

        Args:
            signal_series_ids (List[int | str]): Ids of the signal series

        Returns:
            Result of request as signal series object
        """
        raise Exception("get_signal_series_multidimensional not implemented yet")

    def delete_signal_series(self, signal_series_id: Union[int, str]):
        """
        Send request to graph api to delete given signal series

        Args:
            signal_series_id (int | str): identity of signal series

        Returns:
            Result of request as signal series object
        """
        raise Exception("delete_signal_series not implemented yet")

    def update_signal_series(self, signal_series_id: Union[int, str], signal_series: SignalSeriesPropertyIn):
        """
        Send request to graph api to update given signal series

        Args:
            signal_series_id (int | str): identity of signal series
            signal_series (SignalSeriesPropertyIn): Properties to update

        Returns:
            Result of request as signal series object
        """
        raise Exception("update_signal_series not implemented yet")

    def update_signal_series_relationships(self, signal_series_id: Union[int, str],
                                         signal_series: SignalSeriesRelationIn):
        """
        Send request to graph api to update given signal series

        Args:
            signal_series_id (int | str): identity of signal series
            signal_series (SignalSeriesRelationIn): Relationships to update

        Returns:
            Result of request as signal series object
        """
        raise Exception("update_signal_series_relationships not implemented yet")
