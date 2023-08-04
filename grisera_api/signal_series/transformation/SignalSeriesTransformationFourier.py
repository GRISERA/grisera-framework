from typing import List, Optional
from scipy.signal import welch
from property.property_model import PropertyIn
from signal_series.ts_helpers import get_node_property
from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesIn, SignalIn, Type, TransformationType, \
    SignalValueNodesIn
from signal_series.transformation.SignalSeriesTransformation import SignalSeriesTransformation


class SignalSeriesTransformationFourier(SignalSeriesTransformation):
    """
    Class with logic of signal series resampling transformation

    """

    def transform(self, signal_series: List[SignalSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform signal series data

        Args:
            signal_series (List[SignalSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New time series object
        """
        assert len(
            signal_series) == 1, "Number of time series should equals 1 for resample transformation"
        assert signal_series[0].type == Type.timestamp
        assert len(signal_series[0].signal_values) >= 10
        # przyjmij, ze sa resampled narazie

        # get all timestamps and select proper period :)
        # get all resampled values
        if additional_properties is None:
            additional_properties = []
        additional_properties.append(PropertyIn(
            key="transformation_name", value=TransformationType.FOURIER))

        new_signal_values = []
        new_signal_values_id_mapping = []
        current_signal_value_index = 0
        signal_series = signal_series[0]
        signal_values = []

        period = (int(get_node_property(signal_series.signal_values[1]["timestamp"], "timestamp")) -
                  int(get_node_property(signal_series.signal_values[0]["timestamp"], "timestamp")))*1000
        for current_signal_value_x in signal_series.signal_values:
            signal_values.append(float(get_node_property(
                current_signal_value_x["signal_value"], "value")))
        frequency_signal_values, frequencystamps = welch(
            signal_values, fs=period, nperseg=len(signal_series.signal_values)*2-2, scaling="spectrum")
        for current_signal_value_x in frequency_signal_values:
            new_signal_values.append(SignalIn(signal_value=SignalValueNodesIn(value=current_signal_value_x),
                                              frequencystamp=int(frequencystamps[current_signal_value_index])))
            new_signal_values_id_mapping.append(
                [signal_series.signal_values[current_signal_value_index]["signal_value"]["id"]])
            current_signal_value_index = current_signal_value_index + 1

        return SignalSeriesIn(type=Type.frequencystamp,
                              additional_properties=additional_properties,
                              signal_values=new_signal_values
                              ), new_signal_values_id_mapping
