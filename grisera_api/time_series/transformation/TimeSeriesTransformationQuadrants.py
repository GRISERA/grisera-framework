from typing import List, Optional

from property.property_model import PropertyIn
from time_series.ts_helpers import get_node_property, get_additional_parameter
from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesIn, SignalIn, Type, TransformationType, \
    SignalValueNodesIn
from time_series.transformation.TimeSeriesTransformation import TimeSeriesTransformation


class TimeSeriesTransformationQuadrants(TimeSeriesTransformation):
    """
    Class with logic of time series quadrants transformation

    """

    def transform(self, signal_series: List[SignalSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform time series data.

        Get quadrants for (X, Y) signal values pairs matched by timestamp values.
        This transformation will ignore all signal values which timestamps will not be equal.

        Args:
            time_series (List[SignalSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New time series object
        """
        assert len(signal_series) == 2, "Number of time series should equals 2 for quadrants transformation"
        assert signal_series[0].type == signal_series[1].type, "Time series types should be equal"
        origin_x = get_additional_parameter(additional_properties, "origin_x")
        origin_y = get_additional_parameter(additional_properties, "origin_y")
        origin_x = int(origin_x) if origin_x is not None else 0
        origin_y = int(origin_y) if origin_y is not None else 0

        if additional_properties is None:
            additional_properties = []
        additional_properties.append(PropertyIn(key="transformation_name", value=TransformationType.QUADRANTS))

        new_signal_values = []
        new_signal_values_id_mapping = []
        current_signal_value_y_index = 0
        timestamp_label = "timestamp" if signal_series[0].type == Type.timestamp else "start_timestamp"
        # Iterate over all X signal values
        for current_signal_value_x in signal_series[0].signal_values:
            # For current X signal value find first Y signal value with greater or equal timestamp value
            # If not found, return not existing index
            while current_signal_value_y_index < len(signal_series[1].signal_values) and \
                    int(get_node_property(signal_series[1].signal_values[current_signal_value_y_index]["timestamp"],
                                          timestamp_label)) < int(
                get_node_property(current_signal_value_x["timestamp"], timestamp_label)):
                current_signal_value_y_index += 1
            # Check if X and Y signal timestamps are the same
            if current_signal_value_y_index < len(signal_series[1].signal_values) and \
                    get_node_property(current_signal_value_x["timestamp"], "timestamp") == get_node_property(
                signal_series[1].signal_values[current_signal_value_y_index]["timestamp"], "timestamp") and \
                    get_node_property(current_signal_value_x["timestamp"], "start_timestamp") == get_node_property(
                signal_series[1].signal_values[current_signal_value_y_index]["timestamp"], "start_timestamp") and \
                    get_node_property(current_signal_value_x["timestamp"], "end_timestamp") == get_node_property(
                signal_series[1].signal_values[current_signal_value_y_index]["timestamp"], "end_timestamp"):
                # Determine quadrant comparing X and Y signal values with origin point
                x_positive = 1 if int(
                    get_node_property(current_signal_value_x["signal_value"], "value")) >= origin_x else 0
                y_positive = 1 if int(
                    get_node_property(signal_series[1].signal_values[current_signal_value_y_index]["signal_value"],
                                      "value")) >= origin_y else 0
                quadrant = 1 + [(1, 1), (0, 1), (0, 0), (1, 0)].index((x_positive, y_positive))
                new_signal_values.append(SignalIn(signal_value=SignalValueNodesIn(value=quadrant),
                                                  timestamp=get_node_property(
                                                      current_signal_value_x["timestamp"], "timestamp"),
                                                  start_timestamp=get_node_property(
                                                      current_signal_value_x["timestamp"], "start_timestamp"),
                                                  end_timestamp=get_node_property(
                                                      current_signal_value_x["timestamp"], "end_timestamp"),
                                                  ))
                new_signal_values_id_mapping.append([
                    current_signal_value_x["signal_value"]["id"],
                    signal_series[1].signal_values[current_signal_value_y_index]["signal_value"]["id"]
                ])

        return SignalSeriesIn(type=signal_series[0].type,
                            additional_properties=additional_properties,
                            signal_values=new_signal_values
                            ), new_signal_values_id_mapping
