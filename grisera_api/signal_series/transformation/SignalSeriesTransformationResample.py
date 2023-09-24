from typing import List, Optional

from property.property_model import PropertyIn
from signal_series.ss_helpers import get_node_property, get_additional_parameter
from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesIn, Type, SignalIn, TransformationType, \
    SignalValueNodesIn
from signal_series.transformation.SignalSeriesTransformation import SignalSeriesTransformation


class SignalSeriesTransformationResample(SignalSeriesTransformation):
    """
    Class with logic of signal series resampling transformation

    """

    def transform(self, signal_series: List[SignalSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform signal series data.

        Get Signal_Values with new sampling period.
        This transformation will find the nearest Signal_Value including values in the future.

        Args:
            signal_series (List[SignalSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New signal series object
        """
        assert len(
            signal_series) == 1, "Number of time series should equals 1 for resample transformation"
        period = get_additional_parameter(additional_properties, "period")
        assert period is not None, "period additional parameter is required"
        period = int(period)
        begin_timestamp_label = "timestamp" if signal_series[
            0].type == Type.timestamp else "start_timestamp"
        end_timestamp_label = "timestamp" if signal_series[
            0].type == Type.timestamp else "end_timestamp"
        start_timestamp = get_additional_parameter(
            additional_properties, "start_timestamp")
        end_timestamp = get_additional_parameter(
            additional_properties, "end_timestamp")

        start_timestamp = int(
            start_timestamp) if start_timestamp is not None else 0
        end_timestamp = int(end_timestamp) if end_timestamp is not None else (period + int(
            get_node_property(signal_series[0].signal_values[-1]["timestamp"], end_timestamp_label)))

        if additional_properties is None:
            additional_properties = []
        additional_properties.append(PropertyIn(
            key="transformation_name", value=TransformationType.RESAMPLE_NEAREST))

        new_signal_values = []
        new_signal_values_id_mapping = []
        current_time = start_timestamp
        current_signal_value_index = 0
        if len(signal_series[0].signal_values) > 0:
            while current_time < end_timestamp:
                # For current timestamp find first Signal_Value with greater or equal begin timestamp value
                # If not found, return last Signal_Value
                while current_signal_value_index + 1 < len(signal_series[0].signal_values) and \
                        int(get_node_property(signal_series[0].signal_values[current_signal_value_index]["timestamp"],
                                              begin_timestamp_label)) < current_time:
                    current_signal_value_index += 1
                new_signal_value_index = current_signal_value_index
                if current_signal_value_index > 0:
                    # Get timestamps of found Signal_Value (mostly greater or equal current_time)
                    # and preceding Signal_Value (less than current_time)
                    after_signal_value_timestamp = int(
                        get_node_property(signal_series[0].signal_values[current_signal_value_index]["timestamp"],
                                          begin_timestamp_label))
                    before_signal_value_timestamp = int(
                        get_node_property(signal_series[0].signal_values[current_signal_value_index - 1]["timestamp"],
                                          end_timestamp_label))
                    # Determine which of two Signal_Values is nearer
                    if abs(current_time - before_signal_value_timestamp) <= abs(
                            after_signal_value_timestamp - current_time):
                        new_signal_value_index = current_signal_value_index - 1
                new_signal_values.append(SignalIn(signal_value=SignalValueNodesIn(value=int(
                    get_node_property(signal_series[0].signal_values[new_signal_value_index]["signal_value"], "value"))),
                    timestamp=current_time))
                new_signal_values_id_mapping.append(
                    [signal_series[0].signal_values[new_signal_value_index]["signal_value"]["id"]])
                current_time += period

        return SignalSeriesIn(type=Type.timestamp,
                              additional_properties=additional_properties,
                              signal_values=new_signal_values
                              ), new_signal_values_id_mapping
