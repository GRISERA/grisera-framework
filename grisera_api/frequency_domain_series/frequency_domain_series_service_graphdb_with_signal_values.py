from typing import List, Union, Optional

from starlette.datastructures import QueryParams

from models.not_found_model import NotFoundByIdModel
from signal_series.signal_series_model import Type, SignalSeriesIn, SignalIn, SignalValueNodesIn, \
    StampNodesIn, SignalSeriesTransformationIn
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB
from signal_series.signal_series_service_graphdb_with_signal_values import SignalSeriesServiceGraphDBWithSignalValues


class FrequencyDomainSeriesServiceGraphDBWithSignalValues(SignalSeriesServiceGraphDBWithSignalValues):
    
    def __init__(self):
        super().__init__("frequencystamp", "Frequencystamp","Frequency_Domain_Series")

    def save_signal_series(self, signal_series: SignalSeriesIn):
        """
        Send request to graph api to create new frequency domain series
        Args:
            signal_series (SignalSeriesIn): Frequency Domain series to be added
        Returns:
            Result of request as frequency domain series object
        """
        return super().save_signal_series(signal_series)

    def transform_signal_series(self, signal_series_transformation: SignalSeriesTransformationIn):
        """
        Send request to graph api to create new transformed frequency domain series

        Args:
            signal_series_transformation (SignalSeriesTransformationIn): Frequency Domain series transformation parameters

        Returns:
            Result of request as frequency domain series object
        """
        return super().transform_signal_series(signal_series_transformation)

    def get_experiment_id(self, signal_series_id: int):
        return super().get_experiment_id(signal_series_id)

    def get_neighbour_node_id(self, node_id: int, relation_name: str, forward: bool = True):
        return super().get_neighbour_node_id(node_id,relation_name,forward)

    def get_neighbour_node(self, node_id: int, relation_name: str, forward: bool = True):
        return super().get_neighbour_node(node_id,relation_name,forward)

    def get_or_create_stamp_node(self, stamp_value: int, stamp):
        return super().get_or_create_stamp_node(stamp_value,stamp)

    def create_signal_value(self, signal_value: SignalValueNodesIn, previous_signal_value_node, signal_series_id: int):
        return super().create_signal_value(signal_value,previous_signal_value_node,signal_series_id)

    def save_signal_values(self, signal_values: List[SignalIn], signal_series_id: int, experiment_id: int,
                           stamp_type: Type):
        return super().save_signal_values(signal_values,signal_series_id,experiment_id,stamp_type)


    def get_signal_series(self, signal_series_id: Union[int, str], depth: int = 0,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None):
        """
        Send request to graph api to get given frequency domain series
        Args:
            signal_series_id (int | str): identity of frequency domain series
            depth: (int): specifies how many related entities will be traversed to create the response
            signal_min_value (Optional[int]): Filter Signal_Values by min value
            signal_max_value (Optional[int]): Filter Signal_Values by max value
        Returns:
            Result of request as frequency domain series object
        """
        return super().get_signal_series(signal_series_id,depth,signal_min_value,signal_max_value)

    def get_signal_series_multidimensional(self, signal_series_ids: List[Union[int, str]]):
        """
        Send request to graph api to get given frequency domain series
        Args:
            signal_series_ids (int | str): Ids of the frequency domain series
        Returns:
            Result of request as frequency domain series object
        """
        return super().get_signal_series_multidimensional(signal_series_ids)

    def get_signal_values(self, signal_series_id: Union[int, str], signal_series_type: str,
                          signal_min_value: Optional[int] = None,
                          signal_max_value: Optional[int] = None):
        """
        Send requests to graph api to get all Signal_Values
        Args:
            signal_series_id (int | str): identity of the frequency domain series
            signal_series_type (str): type of the frequency domain series
            signal_min_value (Optional[int]): Filter Signal_Values by min value
            signal_max_value (Optional[int]): Filter Signal_Values by max value
        Returns:
            Array of Signal_Value objects
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
        query_frequencystamp = {
            "nodes": [
                {
                    "id": signal_series_id,
                    "label": "Frequency_Domain_Series"
                },
                {
                    "label": "Signal_Value"
                },
                {
                    "label": "Signal_Value",
                    "result": True,
                    "parameters": parameters
                },
                {
                    "label": "Frequencystamp",
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
                    "label": "inHz"
                }
            ]
        }
        response = self.graph_api_service.get_nodes_by_query(query_frequencystamp)
        signal_values = []
        for row in response["rows"]:
            if signal_series_type == Type.frequencystamp:
                signal_values.append({'signal_value': row[0], 'frequencystamp': row[1]})
        return signal_values

    def get_signal_series_nodes(self, params: QueryParams = None):
        """
        Send request to graph api to get frequency domain series nodes

        Returns:
            Result of request as list of frequency domain series nodes objects
        """
        return super().get_signal_series_nodes(params)

    def delete_signal_series(self, signal_series_id: int):
        """
        Send request to graph api to delete given frequency domain series

        Args:
            signal_series_id (int): Id of frequency domain series

        Returns:
            Result of request as frequency domain series object
        """
        get_response = self.graphdb_service.delete_signal_series(signal_series_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        stamp_ids_to_analyze = []
        for signal_value in get_response.signal_values:
            self.graph_api_service.delete_node(signal_value["signal_value"]["id"])
            if get_response.type == Type.frequencystamp.value:
                stamp_ids_to_analyze.append(signal_value[self.property_stamp_name]["id"])
        for stamp_id in stamp_ids_to_analyze:
            neighbour_signal_a_id, _ = self.get_neighbour_node_id(stamp_id, "inHz")
            if neighbour_signal_a_id is None:
                next_stamp_id, _ = self.get_neighbour_node_id(stamp_id, "next")
                previous_stamp_id, _ = self.get_neighbour_node_id(stamp_id, "next", False)
                previous_experiment_id, _ = self.get_neighbour_node_id(stamp_id, "takes", False)

                self.graph_api_service.delete_node(stamp_id)

                if next_stamp_id is not None:
                    if previous_experiment_id is not None:
                        self.graph_api_service.create_relationships(start_node=previous_experiment_id,
                                                                    end_node=next_stamp_id,
                                                                    name="takes")
                    elif previous_stamp_id is not None:
                        self.graph_api_service.create_relationships(start_node=previous_stamp_id,
                                                                    end_node=next_stamp_id,
                                                                    name="next")
        return get_response
    
    def get_stamp_nodes_in(self,stamp_value):
        return StampNodesIn(frequencystamp=stamp_value)
    
    def get_current_stamp(self,stamp_type,signal_value,stamp):
        if stamp_type == Type.frequencystamp:
            return self.get_or_create_stamp_node(signal_value.frequencystamp,stamp)
    
    def create_relation_nodes(self,stamp_type,current_signal_value_node,signal_value,current_stamp):
        if stamp_type == Type.frequencystamp:
            self.graph_api_service.create_relationships(start_node=current_stamp["id"],
                                                        end_node=current_signal_value_node["id"],
                                                        name="inHz")
        return current_stamp
    
    def get_stamp_value(self, stamp):
        return float(stamp)
    

