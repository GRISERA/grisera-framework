import unittest

from signal_series.signal_series_model import SignalSeriesOut, Type, SignalSeriesMultidimensionalOut
from time_series.transformation.multidimensional.TimeSeriesTransformationMultidimensional import \
    TimeSeriesTransformationMultidimensional


class TestTimeSeriesTransformationMultidimensional(unittest.TestCase):
    time_series_timestamp = [
        SignalSeriesOut(
            type=Type.timestamp,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                     'properties': [{'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                        {'key': 'timestamp', 'value': '0'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 0,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 0, 'properties': [
                        {'key': 'timestamp', 'value': '1'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                     'properties': [
                                         {'key': 'value', 'value': '15'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 6,
                                     'properties': [
                                         {'key': 'value', 'value': '20'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 5, 'properties': [
                        {'key': 'timestamp', 'value': '3'}]}
                }
            ]),
        SignalSeriesOut(
            type=Type.timestamp,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 12,
                                     'properties': [{'key': 'value', 'value': '20'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 11, 'properties': [
                        {'key': 'timestamp', 'value': '0'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 14,
                                     'properties': [
                                         {'key': 'value', 'value': '25'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 13, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 16,
                                     'properties': [
                                         {'key': 'value', 'value': '30'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 15, 'properties': [
                        {'key': 'timestamp', 'value': '3'}]}
                }
            ]),
        SignalSeriesOut(
            type=Type.timestamp,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 22,
                                     'properties': [{'key': 'value', 'value': '35'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 21, 'properties': [
                        {'key': 'timestamp', 'value': '0'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 24,
                                     'properties': [
                                         {'key': 'value', 'value': '40'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 23, 'properties': [
                        {'key': 'timestamp', 'value': '1'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 16,
                                     'properties': [
                                         {'key': 'value', 'value': '45'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 25, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                }
            ])
    ]

    time_series_epoch = [
        SignalSeriesOut(
            type=Type.epoch,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                     'properties': [{'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                        {'key': 'start_timestamp', 'value': 1},
                        {'key': 'end_timestamp', 'value': 4}
                    ]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'start_timestamp', 'value': 15},
                        {'key': 'end_timestamp', 'value': 20}
                    ]}
                }
            ]),
        SignalSeriesOut(
            type=Type.epoch,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 12,
                                     'properties': [{'key': 'value', 'value': '15'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 11, 'properties': [
                        {'key': 'start_timestamp', 'value': 1},
                        {'key': 'end_timestamp', 'value': 4}
                    ]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 14,
                                     'properties': [
                                         {'key': 'value', 'value': '20'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 13, 'properties': [
                        {'key': 'start_timestamp', 'value': 5},
                        {'key': 'end_timestamp', 'value': 10}
                    ]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 16,
                                     'properties': [
                                         {'key': 'value', 'value': '25'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 15, 'properties': [
                        {'key': 'start_timestamp', 'value': 15},
                        {'key': 'end_timestamp', 'value': 20}
                    ]}
                }
            ])
    ]

    def test_transform_timestamp(self):
        time_series_transformation = TimeSeriesTransformationMultidimensional()
        result = time_series_transformation.transform(self.time_series_timestamp)

        self.assertEqual(
            SignalSeriesMultidimensionalOut(
                signal_values=[
                    {
                        'timestamp': {'labels': ['Timestamp'], 'id': 1,
                                      'properties': [{'key': 'timestamp', 'value': '0'}]},
                        'signal_values': [
                            {'labels': ['Signal Value'], 'id': 2, 'properties': [{'key': 'value', 'value': '5'}]},
                            {'labels': ['Signal Value'], 'id': 12, 'properties': [{'key': 'value', 'value': '20'}]},
                            {'labels': ['Signal Value'], 'id': 22, 'properties': [{'key': 'value', 'value': '35'}]}
                        ]},
                    {
                        'timestamp': {'labels': ['Timestamp'], 'id': 3,
                                      'properties': [{'key': 'timestamp', 'value': '2'}]},
                        'signal_values': [
                            {'labels': ['Signal Value'], 'id': 4, 'properties': [{'key': 'value', 'value': '15'}]},
                            {'labels': ['Signal Value'], 'id': 14, 'properties': [{'key': 'value', 'value': '25'}]},
                            {'labels': ['Signal Value'], 'id': 16, 'properties': [{'key': 'value', 'value': '45'}]}
                        ]}
                ]
            ),
            result)

    def test_transform_epoch(self):
        time_series_transformation = TimeSeriesTransformationMultidimensional()
        result = time_series_transformation.transform(self.time_series_epoch)

        self.assertEqual(
            SignalSeriesMultidimensionalOut(
                signal_values=[
                    {
                        'timestamp': {'labels': ['Timestamp'], 'id': 1,
                                      'properties': [{'key': 'start_timestamp', 'value': 1},
                                                     {'key': 'end_timestamp', 'value': 4}]},
                        'signal_values': [
                            {'labels': ['Signal Value'], 'id': 2, 'properties': [{'key': 'value', 'value': '5'}]},
                            {'labels': ['Signal Value'], 'id': 12, 'properties': [{'key': 'value', 'value': '15'}]}
                        ]},
                    {
                        'timestamp': {'labels': ['Timestamp'], 'id': 3,
                                      'properties': [{'key': 'start_timestamp', 'value': 15},
                                                     {'key': 'end_timestamp', 'value': 20}]},
                        'signal_values': [
                            {'labels': ['Signal Value'], 'id': 4, 'properties': [{'key': 'value', 'value': '10'}]},
                            {'labels': ['Signal Value'], 'id': 16, 'properties': [{'key': 'value', 'value': '25'}]}
                        ]}
                ]
            ),
            result)
