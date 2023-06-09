from typing import List, Union, Optional

from starlette.datastructures import QueryParams

from models.not_found_model import NotFoundByIdModel
from time_series.ts_helpers import get_node_property
from signal_series.signal_series_model import Type, SignalSeriesIn, SignalSeriesOut, SignalIn, SignalValueNodesIn, \
    StampNodesIn, SignalSeriesNodesOut, BasicSignalSeriesOut, SignalSeriesTransformationIn, \
    SignalSeriesTransformationRelationshipIn, SignalSeriesMultidimensionalOut
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from signal_series.signal_series_service_graphdb_with_signal_values import SignalSeriesServiceGraphDBWithSignalValues
from time_series.transformation.TimeSeriesTransformationFactory import TimeSeriesTransformationFactory
from time_series.transformation.multidimensional.TimeSeriesTransformationMultidimensional import \
    TimeSeriesTransformationMultidimensional


class TimeSeriesServiceGraphDBWithSignalValues(SignalSeriesServiceGraphDBWithSignalValues):
    
    def __init__(self):
        super().__init__(TimeSeriesServiceGraphDB())

    def save_time_series(self, time_series: SignalSeriesIn):
        """
        Send request to graph api to create new time series
        Args:
            time_series (SignalSeriesIn): Time series to be added
        Returns:
            Result of request as time series object
        """
        return super().save_time_series(time_series)

    def transform_time_series(self, time_series_transformation: SignalSeriesTransformationIn):
        """
        Send request to graph api to create new transformed time series

        Args:
            time_series_transformation (SignalSeriesTransformationIn): Time series transformation parameters

        Returns:
            Result of request as time series object
        """
        return super().transform_time_series(time_series_transformation)

    def get_experiment_id(self, time_series_id: int):
        return super().get_experiment_id(time_series_id)

    def get_neighbour_node_id(self, node_id: int, relation_name: str, forward: bool = True):
        return super().get_neighbour_node_id(node_id,relation_name,forward)

    def get_neighbour_node(self, node_id: int, relation_name: str, forward: bool = True):
        return super().get_neighbour_node(node_id,relation_name,forward)

    def get_or_create_timestamp_node(self, timestamp_value: int, timestamp):
        return super().get_or_create_timestamp_node(timestamp_value,timestamp)

    def create_signal_value(self, signal_value: SignalValueNodesIn, previous_signal_value_node, time_series_id: int):
        return super().create_signal_value(signal_value,previous_signal_value_node,time_series_id)

    def save_signal_values(self, signal_values: List[SignalIn], time_series_id: int, experiment_id: int,
                           timestamp_type: Type):
        return super().save_signal_values(signal_values,time_series_id,experiment_id,timestamp_type)


    def get_time_series(self, time_series_id: Union[int, str], depth: int = 0,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None):
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
        return super().get_time_series(time_series_id,depth,signal_min_value,signal_max_value)

    def get_time_series_multidimensional(self, time_series_ids: List[Union[int, str]]):
        """
        Send request to graph api to get given time series
        Args:
            time_series_ids (int | str): Ids of the time series
        Returns:
            Result of request as time series object
        """
        return super().get_time_series_multidimensional(time_series_ids)

    def get_signal_values(self, time_series_id: Union[int, str], time_series_type: str,
                          signal_min_value: Optional[int] = None,
                          signal_max_value: Optional[int] = None):
        """
        Send requests to graph api to get all signal values
        Args:
            time_series_id (int | str): identity of the time series
            time_series_type (str): type of the time series
            signal_min_value (Optional[int]): Filter signal values by min value
            signal_max_value (Optional[int]): Filter signal values by max value
        Returns:
            Array of signal value objects
        """
        return super().get_signal_values(time_series_id,time_series_type,signal_min_value,signal_max_value)

    def get_time_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        return super().get_time_series_nodes(params)

    def delete_time_series(self, time_series_id: int):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        return super().delete_time_series(time_series_id)
