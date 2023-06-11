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
        super().__init__(TimeSeriesServiceGraphDB(), "timestamp", "Timestamp","Time Series")

    def save_signal_series(self, time_series: SignalSeriesIn):
        """
        Send request to graph api to create new time series
        Args:
            time_series (SignalSeriesIn): Time series to be added
        Returns:
            Result of request as time series object
        """
        return super().save_signal_series(time_series)

    def transform_signal_series(self, time_series_transformation: SignalSeriesTransformationIn):
        """
        Send request to graph api to create new transformed time series

        Args:
            time_series_transformation (SignalSeriesTransformationIn): Time series transformation parameters

        Returns:
            Result of request as time series object
        """
        return super().transform_signal_series(time_series_transformation)

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


    def get_signal_series(self, time_series_id: Union[int, str], depth: int = 0,
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
        return super().get_signal_series(time_series_id,depth,signal_min_value,signal_max_value)

    def get_signal_series_multidimensional(self, time_series_ids: List[Union[int, str]]):
        """
        Send request to graph api to get given time series
        Args:
            time_series_ids (int | str): Ids of the time series
        Returns:
            Result of request as time series object
        """
        return super().get_signal_series_multidimensional(time_series_ids)

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
        parameters = []
        if signal_min_value is not None:
            parameters.append({
                "key": "value",
                "operator": "greater",
                "value": signal_min_value
            })
        if signal_max_value is not None:
            parameters.append({
                "key": "value",
                "operator": "less",
                "value": signal_max_value
            })
        query_timestamp = {
            "nodes": [
                {
                    "id": time_series_id,
                    "label": "Time Series"
                },
                {
                    "label": "Signal Value"
                },
                {
                    "label": "Signal Value",
                    "result": True,
                    "parameters": parameters
                },
                {
                    "label": "Timestamp",
                    "result": True
                }
            ],
            "relations": [
                {
                    "begin_node_index": 0,
                    "end_node_index": 1,
                    "label": "hasSignal"
                },
                {
                    "begin_node_index": 1,
                    "end_node_index": 2,
                    "label": "next",
                    "min_count": 0
                },
                {
                    "begin_node_index": 3,
                    "end_node_index": 2,
                    "label": "inSec"
                }
            ]
        }
        query_epoch = {
            "nodes": [
                {
                    "id": time_series_id,
                    "label": "Time Series"
                },
                {
                    "label": "Signal Value"
                },
                {
                    "label": "Signal Value",
                    "result": True,
                    "parameters": parameters
                },
                {
                    "label": "Timestamp",
                    "result": True
                },
                {
                    "label": "Timestamp",
                    "result": True
                }
            ],
            "relations": [
                {
                    "begin_node_index": 0,
                    "end_node_index": 1,
                    "label": "hasSignal"
                },
                {
                    "begin_node_index": 1,
                    "end_node_index": 2,
                    "label": "next",
                    "min_count": 0
                },
                {
                    "begin_node_index": 3,
                    "end_node_index": 2,
                    "label": "startInSec"
                },
                {
                    "begin_node_index": 4,
                    "end_node_index": 2,
                    "label": "endInSec"
                }
            ]
        }
        response = self.graph_api_service.get_nodes_by_query(
            query_timestamp if time_series_type == Type.timestamp.value else query_epoch)
        signal_values = []
        for row in response["rows"]:
            if time_series_type == Type.timestamp:
                signal_values.append({'signal_value': row[0], 'timestamp': row[1]})
            else:
                signal_values.append({'signal_value': row[0], 'start_timestamp': row[1], 'end_timestamp': row[2]})
        return signal_values

    def get_signal_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        return super().get_signal_series_nodes(params)

    def delete_signal_series(self, time_series_id: int):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        get_response = self.graphdb_service.delete_signal_series(time_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        timestamp_ids_to_analyze = []
        for signal_value in get_response.signal_values:
            self.graph_api_service.delete_node(signal_value["signal_value"]["id"])
            if get_response.type == Type.timestamp.value:
                timestamp_ids_to_analyze.append(signal_value[self.property_stamp_name]["id"])
            else:
                timestamp_ids_to_analyze.append(signal_value["start_timestamp"]["id"])
                timestamp_ids_to_analyze.append(signal_value["end_timestamp"]["id"])
        for timestamp_id in timestamp_ids_to_analyze:
            neighbour_signal_a_id, _ = self.get_neighbour_node_id(timestamp_id, "inSec")
            neighbour_signal_b_id, _ = self.get_neighbour_node_id(timestamp_id, "startInSec")
            neighbour_signal_c_id, _ = self.get_neighbour_node_id(timestamp_id, "endInSec")
            if neighbour_signal_a_id is None and neighbour_signal_b_id is None and neighbour_signal_c_id is None:
                next_timestamp_id, _ = self.get_neighbour_node_id(timestamp_id, "next")
                previous_timestamp_id, _ = self.get_neighbour_node_id(timestamp_id, "next", False)
                previous_experiment_id, _ = self.get_neighbour_node_id(timestamp_id, "takes", False)

                self.graph_api_service.delete_node(timestamp_id)

                if next_timestamp_id is not None:
                    if previous_experiment_id is not None:
                        self.graph_api_service.create_relationships(start_node=previous_experiment_id,
                                                                    end_node=next_timestamp_id,
                                                                    name="takes")
                    elif previous_timestamp_id is not None:
                        self.graph_api_service.create_relationships(start_node=previous_timestamp_id,
                                                                    end_node=next_timestamp_id,
                                                                    name="next")
        return get_response
    
    def get_stamp_nodes_in(self,timestamp_value):
        return StampNodesIn(timestamp=timestamp_value)
    
    def get_current_stamp(self,timestamp_type,signal_value,timestamp):
        if timestamp_type == Type.timestamp:
            return self.get_or_create_timestamp_node(signal_value.timestamp,timestamp)
        return self.get_or_create_timestamp_node(signal_value.start_timestamp, timestamp)
    
    def create_relation_nodes(self,timestamp_type,current_signal_value_node,signal_value,current_timestamp):
        if timestamp_type == Type.timestamp:
            self.graph_api_service.create_relationships(start_node=current_timestamp["id"],
                                                        end_node=current_signal_value_node["id"],
                                                        name="inSec")
        else:
            self.graph_api_service.create_relationships(start_node=current_timestamp["id"],
                                                        end_node=current_signal_value_node["id"],
                                                        name="startInSec")
            current_timestamp = self.get_or_create_timestamp_node(signal_value.end_timestamp, current_timestamp)

            if current_timestamp["errors"] is not None:
                return current_timestamp["errors"]

            self.graph_api_service.create_relationships(start_node=current_timestamp["id"],
                                                        end_node=current_signal_value_node["id"],
                                                        name="endInSec")
        return current_timestamp
