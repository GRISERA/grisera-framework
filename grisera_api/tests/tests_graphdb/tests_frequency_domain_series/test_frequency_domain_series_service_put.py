import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut
from observable_information.observable_information_model import BasicObservableInformationOut
from signal_series.signal_series_model import *
from models.not_found_model import *

from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB
from graph_api_service import GraphApiService


class TestFrequencyDomainSeriesServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    def test_update_signal_series_without_error(self, delete_node_properties_mock,
                                                get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}

        get_node_mock.return_value = {'id': id_node, 'labels': ['Frequency Domain Series'],
                                      'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                     {'key': 'source',
                                                         'value': "cos"},
                                                     {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        frequency_domain_series_in = SignalSeriesPropertyIn(
            type="Frequencystamp", source="cos", additional_properties=additional_properties)
        frequency_domain_series_out = BasicSignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", additional_properties=additional_properties)
        calls = [mock.call(1)]
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.update_signal_series(
            id_node, frequency_domain_series_in)

        self.assertEqual(result, frequency_domain_series_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_called_once_with(
            id_node, frequency_domain_series_in)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_signal_series_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        additional_properties = [PropertyIn(key='identifier', value=5)]
        frequency_domain_series_in = SignalSeriesPropertyIn(
            type="Frequencystamp", source="cos", additional_properties=additional_properties)
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.update_signal_series(
            id_node, frequency_domain_series_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_signal_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {
            'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        additional_properties = [PropertyIn(key='identifier', value=5)]
        frequency_domain_series_in = SignalSeriesPropertyIn(type="Frequencystamp", source="cos", id=id_node,
                                                            additional_properties=additional_properties)
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.update_signal_series(
            id_node, frequency_domain_series_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
