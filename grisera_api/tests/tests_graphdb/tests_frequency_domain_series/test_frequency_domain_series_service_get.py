import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut
from observable_information.observable_information_model import BasicObservableInformationOut
from signal_series.signal_series_model import *
from models.not_found_model import *

from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB
from graph_api_service import GraphApiService


class TestFrequencyDomainSeriesServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_signal_series_without_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Frequency_Domain_Series'],
                                      'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                     {'key': 'source',
                                                         'value': "cos"},
                                                     {'key': 'test', 'value': 'test2'}],
                                      "errors": None, 'links': None}
        frequency_domain_series = BasicSignalSeriesOut(id=1, type="Frequencystamp", source="cos",
                                                       additional_properties=[{'key': 'test', 'value': 'test2'}])
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.get_signal_series(id_node)

        self.assertEqual(result, frequency_domain_series)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_signal_series_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.get_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_signal_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {
            'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.get_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_signal_series_nodes(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Frequency_Domain_Series'],
                                                  'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                                 {'key': 'source',
                                                                     'value': "cos"},
                                                                 {'key': 'test', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Frequency_Domain_Series'],
                                                  'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                                 {'key': 'source',
                                                                     'value': "cos"},
                                                                 {'key': 'test2', 'value': 'test3'}]}]}
        frequency_domain_series_one = BasicSignalSeriesOut(id=1, type="Frequencystamp", source="cos", additional_properties=[
            PropertyIn(key='test', value='test')])
        frequency_domain_series_two = BasicSignalSeriesOut(id=2, type="Frequencystamp", source="cos", additional_properties=[
            PropertyIn(key='test2', value='test3')])
        frequency_domain_series_nodes = SignalSeriesNodesOut(
            signal_series_nodes=[frequency_domain_series_one, frequency_domain_series_two])
        frequency_domain_series_nodes_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_nodes_service.get_signal_series_nodes()

        self.assertEqual(result, frequency_domain_series_nodes)
        get_nodes_mock.assert_called_once_with("`Frequency_Domain_Series`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_signal_series_nodes_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        frequency_domain_series_nodes = SignalSeriesNodesOut(
            signal_series_nodes=[])
        frequency_domain_series_nodes_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_nodes_service.get_signal_series_nodes()

        self.assertEqual(result, frequency_domain_series_nodes)
        get_nodes_mock.assert_called_once_with("`Frequency_Domain_Series`")
