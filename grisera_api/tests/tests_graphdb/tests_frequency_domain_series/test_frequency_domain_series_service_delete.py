import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut
from observable_information.observable_information_model import BasicObservableInformationOut
from signal_series.signal_series_model import *
from models.not_found_model import *

from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB
from graph_api_service import GraphApiService


class TestFrequencyDomainSeriesServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_without_error(self, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Frequency Domain Series'],
                                                                      'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                                                     {'key': 'source', 'value': "cos"}],
                                                                      "errors": None, 'links': None}
        frequency_domain_series = BasicSignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", additional_properties=[])
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.delete_signal_series(id_node)

        self.assertEqual(result, frequency_domain_series)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.delete_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {
            'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.delete_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
