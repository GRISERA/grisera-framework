import unittest

from property.property_model import PropertyIn
from time_series.time_series_model import TimeSeriesOut, Type, TimeSeriesIn, SignalIn
from time_series.transformation.TimeSeriesTransformationResample import TimeSeriesTransformationResample


class TestTimeSeriesTransformationResample(unittest.TestCase):
    time_series_timestamp = [
        TimeSeriesOut(
            type=Type.timestamp,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                        {'key': 'timestamp', 'value': 0}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                     'properties': [
                                         {'key': 'value', 'value': '20'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'timestamp', 'value': 5}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 6,
                                     'properties': [
                                         {'key': 'value', 'value': '30'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 5, 'properties': [
                        {'key': 'timestamp', 'value': 9}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 8,
                                     'properties': [
                                         {'key': 'value', 'value': '40'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 7, 'properties': [
                        {'key': 'timestamp', 'value': 12}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 10,
                                     'properties': [
                                         {'key': 'value', 'value': '50'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 9, 'properties': [
                        {'key': 'timestamp', 'value': 29}]}
                }
            ])
    ]

    time_series_epoch = [
        TimeSeriesOut(
            type=Type.epoch,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                        {'key': 'start_timestamp', 'value': 1},
                        {'key': 'end_timestamp', 'value': 4}
                    ]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                     'properties': [
                                         {'key': 'value', 'value': '20'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'start_timestamp', 'value': 7},
                        {'key': 'end_timestamp', 'value': 12}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 6,
                                     'properties': [
                                         {'key': 'value', 'value': '30'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 5, 'properties': [
                        {'key': 'start_timestamp', 'value': 23},
                        {'key': 'end_timestamp', 'value': 24}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 8,
                                     'properties': [
                                         {'key': 'value', 'value': '40'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 7, 'properties': [
                        {'key': 'start_timestamp', 'value': 25},
                        {'key': 'end_timestamp', 'value': 30}]}
                }
            ])
    ]

    def test_transform_timestamp(self):
        additional_properties = [PropertyIn(key="period", value="10")]

        time_series_transformation = TimeSeriesTransformationResample()
        result = time_series_transformation.transform(self.time_series_timestamp, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.timestamp,
                    signal_values=[
                        SignalIn(timestamp=0, value='10'),
                        SignalIn(timestamp=10, value='30'),
                        SignalIn(timestamp=20, value='40'),
                        SignalIn(timestamp=30, value='50')
                    ],
                    additional_properties=[
                        PropertyIn(key='period', value='10'),
                        PropertyIn(key='transformation_name', value='resample_nearest')
                    ]
                ),
                [[2], [6], [8], [10]]
            ),
            result)

    def test_transform_timestamp_begin_end_parameters(self):
        additional_properties = [
            PropertyIn(key="period", value="5"),
            PropertyIn(key="start_timestamp", value="3"),
            PropertyIn(key="end_timestamp", value="23")
        ]

        time_series_transformation = TimeSeriesTransformationResample()
        result = time_series_transformation.transform(self.time_series_timestamp, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.timestamp,
                    signal_values=[
                        SignalIn(timestamp=3, value='20'),
                        SignalIn(timestamp=8, value='30'),
                        SignalIn(timestamp=13, value='40'),
                        SignalIn(timestamp=18, value='40')
                    ],
                    additional_properties=[
                        PropertyIn(key="period", value="5"),
                        PropertyIn(key="start_timestamp", value="3"),
                        PropertyIn(key="end_timestamp", value="23"),
                        PropertyIn(key='transformation_name', value='resample_nearest')
                    ]
                ),
                [[4], [6], [8], [8]]
            ),
            result)

    def test_transform_epoch(self):
        additional_properties = [PropertyIn(key="period", value="5")]

        time_series_transformation = TimeSeriesTransformationResample()
        result = time_series_transformation.transform(self.time_series_epoch, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.epoch,
                    signal_values=[
                        SignalIn(timestamp=0, value='10'),
                        SignalIn(timestamp=5, value='10'),
                        SignalIn(timestamp=10, value='20'),
                        SignalIn(timestamp=15, value='20'),
                        SignalIn(timestamp=20, value='30'),
                        SignalIn(timestamp=25, value='40'),
                        SignalIn(timestamp=30, value='40')
                    ],
                    additional_properties=[
                        PropertyIn(key='period', value='5'),
                        PropertyIn(key='transformation_name', value='resample_nearest')
                    ]
                ),
                [[2], [2], [4], [4], [6], [8], [8]]
            ),
            result)

    def test_transform_epoch_begin_end_parameters(self):
        additional_properties = [
            PropertyIn(key="period", value="10"),
            PropertyIn(key="start_timestamp", value="6"),
            PropertyIn(key="end_timestamp", value="36")
        ]

        time_series_transformation = TimeSeriesTransformationResample()
        result = time_series_transformation.transform(self.time_series_epoch, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.epoch,
                    signal_values=[
                        SignalIn(timestamp=6, value='20'),
                        SignalIn(timestamp=16, value='20'),
                        SignalIn(timestamp=26, value='40')
                    ],
                    additional_properties=[
                        PropertyIn(key="period", value="10"),
                        PropertyIn(key="start_timestamp", value="6"),
                        PropertyIn(key="end_timestamp", value="36"),
                        PropertyIn(key='transformation_name', value='resample_nearest')
                    ]
                ),
                [[4], [4], [8]]
            ),
            result)
