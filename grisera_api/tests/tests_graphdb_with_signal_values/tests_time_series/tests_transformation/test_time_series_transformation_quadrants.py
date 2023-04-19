import unittest

from property.property_model import PropertyIn
from time_series.time_series_model import TimeSeriesOut, Type, TimeSeriesIn, SignalIn, SignalValueNodesIn
from time_series.transformation.TimeSeriesTransformationQuadrants import TimeSeriesTransformationQuadrants


class TestTimeSeriesTransformationQuadrants(unittest.TestCase):
    time_series_timestamp = [
        TimeSeriesOut(
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
                                     'properties': [{'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 0, 'properties': [
                        {'key': 'timestamp', 'value': '1'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                     'properties': [
                                         {'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 6,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 5, 'properties': [
                        {'key': 'timestamp', 'value': '3'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 8,
                                     'properties': [
                                         {'key': 'value', 'value': '-10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 7, 'properties': [
                        {'key': 'timestamp', 'value': '4'}]}
                }
            ]),
        TimeSeriesOut(
            type=Type.timestamp,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 12,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 11, 'properties': [
                        {'key': 'timestamp', 'value': '0'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 14,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 13, 'properties': [
                        {'key': 'timestamp', 'value': '2'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 16,
                                     'properties': [
                                         {'key': 'value', 'value': '5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 15, 'properties': [
                        {'key': 'timestamp', 'value': '3'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 18,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 17, 'properties': [
                        {'key': 'timestamp', 'value': '4'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 20,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 19, 'properties': [
                        {'key': 'timestamp', 'value': '5'}]}
                }
            ])
    ]

    time_series_epoch = [
        TimeSeriesOut(
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
                        {'key': 'start_timestamp', 'value': 5},
                        {'key': 'end_timestamp', 'value': 10}
                    ]}
                }
            ]),
        TimeSeriesOut(
            type=Type.epoch,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 12,
                                     'properties': [{'key': 'value', 'value': '10'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 11, 'properties': [
                        {'key': 'start_timestamp', 'value': 1},
                        {'key': 'end_timestamp', 'value': 4}
                    ]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 14,
                                     'properties': [
                                         {'key': 'value', 'value': '-5'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 13, 'properties': [
                        {'key': 'start_timestamp', 'value': 5},
                        {'key': 'end_timestamp', 'value': 10}
                    ]}
                }
            ])
    ]

    def test_transform_timestamp(self):
        additional_properties = []

        time_series_transformation = TimeSeriesTransformationQuadrants()
        result = time_series_transformation.transform(self.time_series_timestamp, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.timestamp,
                    signal_values=[
                        SignalIn(timestamp='0', signal_value=SignalValueNodesIn(value='1')),
                        SignalIn(timestamp='2', signal_value=SignalValueNodesIn(value='4')),
                        SignalIn(timestamp='3', signal_value=SignalValueNodesIn(value='2')),
                        SignalIn(timestamp='4', signal_value=SignalValueNodesIn(value='3'))
                    ],
                    additional_properties=[
                        PropertyIn(key='transformation_name', value='quadrants')
                    ]
                ),
                [[2, 12], [4, 14], [6, 16], [8, 18]]
            ),
            result)

    def test_transform_timestamp_origin_parameters(self):
        additional_properties = [
            PropertyIn(key="origin_x", value="-6"),
            PropertyIn(key="origin_y", value="6")
        ]

        time_series_transformation = TimeSeriesTransformationQuadrants()
        result = time_series_transformation.transform(self.time_series_timestamp, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.timestamp,
                    signal_values=[
                        SignalIn(timestamp='0', signal_value=SignalValueNodesIn(value='1')),
                        SignalIn(timestamp='2', signal_value=SignalValueNodesIn(value='4')),
                        SignalIn(timestamp='3', signal_value=SignalValueNodesIn(value='4')),
                        SignalIn(timestamp='4', signal_value=SignalValueNodesIn(value='3'))
                    ],
                    additional_properties=[
                        PropertyIn(key="origin_x", value="-6"),
                        PropertyIn(key="origin_y", value="6"),
                        PropertyIn(key='transformation_name', value='quadrants')
                    ]
                ),
                [[2, 12], [4, 14], [6, 16], [8, 18]]
            ),
            result)

    def test_transform_epoch(self):
        additional_properties = []

        time_series_transformation = TimeSeriesTransformationQuadrants()
        result = time_series_transformation.transform(self.time_series_epoch, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.epoch,
                    signal_values=[
                        SignalIn(start_timestamp='1', end_timestamp='4', signal_value=SignalValueNodesIn(value='1')),
                        SignalIn(start_timestamp='5', end_timestamp='10', signal_value=SignalValueNodesIn(value='4'))
                    ],
                    additional_properties=[
                        PropertyIn(key='transformation_name', value='quadrants')
                    ]
                ),
                [[2, 12], [4, 14]]
            ),
            result)

    def test_transform_epoch_origin_parameters(self):
        additional_properties = [
            PropertyIn(key="origin_x", value="7"),
            PropertyIn(key="origin_y", value="-10")
        ]

        time_series_transformation = TimeSeriesTransformationQuadrants()
        result = time_series_transformation.transform(self.time_series_epoch, additional_properties)

        self.assertEqual(
            (
                TimeSeriesIn(
                    type=Type.epoch,
                    signal_values=[
                        SignalIn(start_timestamp='1', end_timestamp='4', signal_value=SignalValueNodesIn(value='2')),
                        SignalIn(start_timestamp='5', end_timestamp='10', signal_value=SignalValueNodesIn(value='1'))
                    ],
                    additional_properties=[
                        PropertyIn(key="origin_x", value="7"),
                        PropertyIn(key="origin_y", value="-10"),
                        PropertyIn(key='transformation_name', value='quadrants')
                    ]
                ),
                [[2, 12], [4, 14]]
            ),
            result)
