import unittest

from property.property_model import PropertyIn
from signal_series.signal_series_model import SignalSeriesOut, Type, SignalSeriesIn, SignalIn, SignalValueNodesIn
from signal_series.transformation.SignalSeriesTransformationFourier import SignalSeriesTransformationFourier


class TestSignalSeriesTransformationFourier(unittest.TestCase):
    time_series_timestamp = [
        SignalSeriesOut(
            type=Type.timestamp,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 2,
                                     'properties': [{'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                        {'key': 'timestamp', 'value': '0'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 0,
                                     'properties': [{'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 0, 'properties': [
                        {'key': 'timestamp', 'value': '1'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 4,
                                     'properties': [
                                         {'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 6,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 5, 'properties': [
                        {'key': 'timestamp', 'value': '3'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 8,
                                     'properties': [
                                         {'key': 'value', 'value': '-10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 7, 'properties': [
                        {'key': 'timestamp', 'value': '4'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 12,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 11, 'properties': [
                        {'key': 'timestamp', 'value': '0'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 14,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 13, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 16,
                                     'properties': [
                                         {'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 15, 'properties': [
                        {'key': 'timestamp', 'value': '3'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 18,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 17, 'properties': [
                        {'key': 'timestamp', 'value': '4'}]}
                },
                {
                    'signal_value': {'labels': ['Signal_Value'], 'id': 20,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 19, 'properties': [
                        {'key': 'timestamp', 'value': '5'}]}
                }
            ])
    ]

    def test_transform_timestamp(self):
        additional_properties = []

        time_series_transformation = SignalSeriesTransformationFourier()
        result = time_series_transformation.transform(
            self.time_series_timestamp, additional_properties)

        self.assertEqual(
            (
                SignalSeriesIn(
                    type=Type.frequencystamp,
                    signal_values=[
                        SignalIn(frequencystamp='0',
                                 signal_value=SignalValueNodesIn(value='0.0')),
                        SignalIn(frequencystamp='1',
                                 signal_value=SignalValueNodesIn(value='100.0')),
                        SignalIn(frequencystamp='13',
                                 signal_value=SignalValueNodesIn(value='200.0')),
                        SignalIn(frequencystamp='19',
                                 signal_value=SignalValueNodesIn(value='300.0')),
                        SignalIn(frequencystamp='42',
                                 signal_value=SignalValueNodesIn(value='400.0')),
                        SignalIn(frequencystamp='19',
                                 signal_value=SignalValueNodesIn(value='500.0'))
                    ],
                    additional_properties=[
                        PropertyIn(key='transformation_name',
                                   value='fourier')
                    ]
                ),
                [[2], [0], [4], [6], [8], [12]]
            ),
            result)
