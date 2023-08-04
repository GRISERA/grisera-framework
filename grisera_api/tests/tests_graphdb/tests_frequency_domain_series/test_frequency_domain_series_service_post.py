import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from measure.measure_service_graphdb import MeasureServiceGraphDB
from observable_information.observable_information_model import BasicObservableInformationOut
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB
from signal_series.signal_series_model import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


def relationship_function(*args, **kwargs):
    if kwargs['name'] == 'hasPublication':
        return {'start_node': 1, 'end_node': 3, 'id': 5, 'name': 'hasPublication', 'errors': ['error']}
    return {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'hasAuthor', 'errors': None}


class TestFrequencyDomainSeriesServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(ObservableInformationServiceGraphDB, 'get_observable_information')
    @mock.patch.object(MeasureServiceGraphDB, 'get_measure')
    def test_save_signal_series_without_errors(self, get_measure_mock, get_observable_information_mock, get_node_mock,
                                               create_relationships_mock, create_properties_mock, create_node_mock):
        id_node = 1
        get_observable_information_mock.return_value = BasicObservableInformationOut(
            id=2)
        get_measure_mock.return_value = None
        get_node_mock.return_value = {'id': id_node, 'labels': ['Frequency Domain Series'],
                                      'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                     {'key': 'source', 'value': "cos"}],
                                      "errors": None, 'links': None}
        create_node_mock.return_value = {
            'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {
            'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasMeasure', 'errors': None}
        frequency_domain_series_in = SignalSeriesIn(
            id=1, type="Frequencystamp", source="cos", observable_information_id=2, measure_id=3)
        frequency_domain_series_out = BasicSignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", additional_properties=[])
        calls = [mock.call(end_node=3, start_node=1, name="hasMeasure")]

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()
        frequency_domain_series_service.observable_information_service = mock.create_autospec(
            ObservableInformationServiceGraphDB)
        frequency_domain_series_service.observable_information_service.get_observable_information = get_observable_information_mock

        frequency_domain_series_service.measure_service = mock.create_autospec(
            MeasureServiceGraphDB)
        frequency_domain_series_service.measure_service.get_measure = get_measure_mock

        result = frequency_domain_series_service.save_signal_series(
            frequency_domain_series_in)

        self.assertEqual(result, frequency_domain_series_out)
        create_node_mock.assert_called_once_with('Frequency Domain Series')
        create_properties_mock.assert_called_once_with(
            id_node, frequency_domain_series_in)
        create_relationships_mock.assert_has_calls([mock.call(start_node=id_node, end_node=2,
                                                              name="hasObservableInformation"),
                                                    mock.call(start_node=id_node, end_node=3,
                                                              name="hasMeasure")])

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_signal_series_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {
            'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        frequency_domain_series = SignalSeriesIn(
            type="Frequencystamp", source="cos", observable_information_id=1, measure_id=2)
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDB()

        result = frequency_domain_series_service.save_signal_series(
            frequency_domain_series)

        self.assertEqual(result, SignalSeriesOut(
            type="Frequencystamp", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('Frequency Domain Series')
