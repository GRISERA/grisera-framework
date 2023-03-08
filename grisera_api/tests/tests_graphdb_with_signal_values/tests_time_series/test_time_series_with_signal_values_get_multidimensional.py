import unittest

from time_series.time_series_model import TimeSeriesOut, Type, \
    TimeSeriesMultidimensionalOut
from time_series.time_series_service_graphdb_with_signal_values import TimeSeriesServiceGraphDBWithSignalValues


class TestTimeSeriesWithSignalValuesServiceGetMultidimensional(unittest.TestCase):
    def test_get_time_series_multidimensional_without_errors(self):
        result_timeseries = TimeSeriesMultidimensionalOut(
            type=Type.timestamp,
            signal_values=[
                {

                    'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                        {'key': 'timestamp', 'value': '100'}]},
                    'signal_values': [
                        {'labels': ['Signal Value'], 'id': 22,
                         'properties': [{'key': 'value', 'value': '10'}]},
                        {'labels': ['Signal Value'], 'id': 12,
                         'properties': [{'key': 'value', 'value': '11'}]}
                    ]
                },
                {

                    'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                        {'key': 'timestamp', 'value': '200'}]},
                    'signal_values': [
                        {'labels': ['Signal Value'], 'id': 4,
                         'properties': [{'key': 'value', 'value': '20'}]},
                        {'labels': ['Signal Value'], 'id': 14,
                         'properties': [{'key': 'value', 'value': '21'}
                                        ]
                         }
                    ]
                }
            ]
        )

        def get_time_series_side_effect(time_series_id: int):
            if time_series_id == 60:
                return TimeSeriesOut(
                    id=time_series_id,
                    type=Type.timestamp,
                    signal_values=[
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 22,
                                             'properties': [
                                                 {'key': 'value', 'value': '10'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 1,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '100'}]}
                        },
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                             'properties': [
                                                 {'key': 'value', 'value': '20'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 3,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '200'}]}
                        }
                    ])
            elif time_series_id == 61:
                return TimeSeriesOut(
                    id=time_series_id,
                    type=Type.timestamp,
                    signal_values=[
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 12,
                                             'properties': [
                                                 {'key': 'value', 'value': '11'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 11,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '100'}]}
                        },
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 14,
                                             'properties': [
                                                 {'key': 'value', 'value': '21'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 13,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '200'}]}
                        }
                    ])
            else:
                return None

        time_series_service = TimeSeriesServiceGraphDBWithSignalValues()
        time_series_service.get_time_series = get_time_series_side_effect
        result = time_series_service.get_time_series_multidimensional([60, 61])

        self.assertEqual(result_timeseries, result)
