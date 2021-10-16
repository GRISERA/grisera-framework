import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from time_series.time_series_model import *
from time_series.time_series_service import TimeSeriesService


class TestTimeSeriesService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_time_series_without_errors(self, create_relationships_mock, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node,
                                               'properties': [{'key': 'type', 'value': 'Epoch'},
                                                              {'key': 'source', 'value': 'cos'}],
                                               "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]
        calls = [mock.call(1, 3, 'hasObservableInformation'), mock.call(1, 5, 'hasMeasure')]

        time_series = TimeSeriesIn(type="Epoch", source="cos", observable_information_id=3, measure_id=5,
                                   additional_properties=additional_properties)

        time_series_service = TimeSeriesService()

        result = time_series_service.save_time_series(time_series)

        self.assertEqual(result, TimeSeriesOut(type="Epoch", source="cos", observable_information_id=3,
                                               measure_id=5, id=1, additional_properties=additional_properties))

        create_node_mock.assert_called_once_with('TimeSeries')
        create_properties_mock.assert_called_once_with(id_node, time_series)
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_time_series_with_time_series_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        time_series = TimeSeriesIn(type="Epoch", source="cos")
        time_series_service = TimeSeriesService()

        result = time_series_service.save_time_series(time_series)

        self.assertEqual(result, TimeSeriesOut(type="Epoch", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('TimeSeries')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_time_series_with_time_series_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        time_series = TimeSeriesIn(type="Epoch", source="cos")
        time_series_service = TimeSeriesService()

        result = time_series_service.save_time_series(time_series)

        self.assertEqual(result, TimeSeriesOut(type="Epoch", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('TimeSeries')
        create_properties_mock.assert_called_once_with(id_node, time_series)
