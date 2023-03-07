from typing import List, Optional

from property.property_model import PropertyIn
from time_series.helpers import get_node_property, get_additional_parameter
from time_series.time_series_model import TimeSeriesOut, TimeSeriesIn, Type, SignalIn
from time_series.transformation.TimeSeriesTransformation import TimeSeriesTransformation, TransformationType


class TimeSeriesTransformationResample(TimeSeriesTransformation):
    """
    Class with logic of time series resampling transformation

    """

    def transform(self, time_series: List[TimeSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform time series data

        Args:
            time_series (List[TimeSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New time series object
        """
        assert len(time_series) == 1, "Number of time series should equals 1 for resample transformation"
        period = get_additional_parameter(additional_properties, "period")
        assert period is not None, "period additional parameter is required"
        period = int(period)
        begin_timestamp_label = "timestamp" if time_series[0].type == Type.timestamp else "start_timestamp"
        end_timestamp_label = "timestamp" if time_series[0].type == Type.timestamp else "end_timestamp"
        start_timestamp = get_additional_parameter(additional_properties, "start_timestamp")
        end_timestamp = get_additional_parameter(additional_properties, "end_timestamp")
        if start_timestamp is None:
            start_timestamp = 0
        else:
            start_timestamp = int(start_timestamp)
        if end_timestamp is not None:
            end_timestamp = int(end_timestamp)
        else:
            end_timestamp = period + int(
                get_node_property(time_series[0].signal_values[-1]["timestamp"], end_timestamp_label))

        if additional_properties is None:
            additional_properties = []
        additional_properties.append(PropertyIn(key="transformation_name", value=TransformationType.RESAMPLE_NEAREST))

        new_signal_values = []
        new_signal_values_index_mapping = []
        current_time = start_timestamp
        current_signal_value_index = 0
        while current_time < end_timestamp:
            while current_signal_value_index + 1 < len(time_series[0].signal_values) and \
                    int(get_node_property(time_series[0].signal_values[current_signal_value_index]["timestamp"],
                                          end_timestamp_label)) <= current_time:
                current_signal_value_index += 1
            if current_signal_value_index < len(time_series[0].signal_values):
                new_signal_value_index = current_signal_value_index
                if current_signal_value_index > 0:
                    after_signal_value_timestamp = int(
                        get_node_property(time_series[0].signal_values[current_signal_value_index]["timestamp"],
                                          begin_timestamp_label))
                    before_signal_value_timestamp = int(
                        get_node_property(time_series[0].signal_values[current_signal_value_index - 1]["timestamp"],
                                          end_timestamp_label))
                    if abs(current_time - before_signal_value_timestamp) <= abs(
                            after_signal_value_timestamp - current_time):
                        new_signal_value_index = current_signal_value_index - 1
                new_signal_values.append(SignalIn(value=int(
                    get_node_property(time_series[0].signal_values[new_signal_value_index]["signal_value"], "value")),
                    timestamp=current_time))
                new_signal_values_index_mapping.append(
                    [time_series[0].signal_values[new_signal_value_index]["signal_value"]["id"]])
                current_time += period

        return TimeSeriesIn(type=time_series[0].type,
                            additional_properties=additional_properties,
                            signal_values=new_signal_values
                            ), new_signal_values_index_mapping
