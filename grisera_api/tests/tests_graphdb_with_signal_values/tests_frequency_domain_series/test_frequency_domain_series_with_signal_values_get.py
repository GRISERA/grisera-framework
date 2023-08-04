import unittest
from unittest import mock

from graph_api_service import GraphApiService
from measure.measure_model import BasicMeasureOut
from models.not_found_model import NotFoundByIdModel
from observable_information.observable_information_model import BasicObservableInformationOut
from property.property_model import PropertyIn
from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesNodesOut, BasicSignalSeriesOut
from frequency_domain_series.frequency_domain_series_service_graphdb_with_signal_values import FrequencyDomainSeriesServiceGraphDBWithSignalValues


class TestTimeSeriesWithSignalValuesServicePost(unittest.TestCase):
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_nodes_by_query')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_signal_series_without_error(self, get_node_relationships_mock, get_nodes_by_query_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Frequency Domain Series'],
                                      'properties': [{'key': 'type', 'value': "Frequencystamp"},
                                                     {'key': 'source',
                                                         'value': "cos"},
                                                     {'key': 'test', 'value': 'test2'}],
                                      "errors": None, 'links': None}
        get_nodes_by_query_mock.return_value = {
            'rows': [
                [{'labels': ['Signal Value'], 'id': 2, 'properties': [{'key': 'value', 'value': '10'}]},
                 {'labels': ['Frequencystamp'], 'id': 1, 'properties': [{'key': 'frequencystamp', 'value': '100'}]}],
                [{'labels': ['Signal Value'], 'id': 4, 'properties': [{'key': 'value', 'value': '20'}]},
                 {'labels': ['Frequencystamp'], 'id': 3, 'properties': [{'key': 'frequencystamp', 'value': '200'}]}],
                [{'labels': ['Signal Value'], 'id': 6, 'properties': [{'key': 'value', 'value': '30'}]},
                 {'labels': ['Frequencystamp'], 'id': 5, 'properties': [{'key': 'frequencystamp', 'value': '300'}]}]
            ],
            'errors': []
        }
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "hasObservableInformation", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 15,
             "name": "hasMeasure", "id": 0,
             "properties": None}]}
        additional_properties = [PropertyIn(key='test', value='test2')]
        frequency_domain_series = BasicSignalSeriesOut(id=1, type="Frequencystamp", source="cos",
                                                       signal_values=[
                                                           {
                                                               'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                                                                'properties': [{'key': 'value', 'value': '10'}]},
                                                               'frequencystamp': {'labels': ['Frequencystamp'], 'id': 1, 'properties': [
                                                                   {'key': 'frequencystamp', 'value': '100'}]}
                                                           },
                                                           {
                                                               'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                                                                'properties': [
                                                                   {'key': 'value', 'value': '20'}]},
                                                               'frequencystamp': {'labels': ['Frequencystamp'], 'id': 3, 'properties': [
                                                                   {'key': 'frequencystamp', 'value': '200'}]}
                                                           },
                                                           {
                                                               'signal_value': {'labels': ['Signal Value'], 'id': 6,
                                                                                'properties': [
                                                                   {'key': 'value', 'value': '30'}]},
                                                               'frequencystamp': {'labels': ['Frequencystamp'], 'id': 5, 'properties': [
                                                                   {'key': 'frequencystamp', 'value': '300'}]}
                                                           }
                                                       ],
                                                       additional_properties=additional_properties,
                                                       observable_informations=[
                                                           BasicObservableInformationOut(**{'id': 19})],
                                                       measure=BasicMeasureOut(id=15, datatype='float', range='<0,1>', unit='cm'))
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()

        result = frequency_domain_series_service.get_signal_series(id_node)

        self.assertEqual(frequency_domain_series, result)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_not_called()

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_signal_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {
            'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()

        result = frequency_domain_series_service.get_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes_by_query')
    def test_get_signal_series_nodes(self, get_nodes_by_query):
        get_nodes_by_query.return_value = {
            'rows': [
                [{'labels': ['Frequency Domain Series'], 'id': 2,
                  'properties': [{'key': 'value', 'value': 'test1'}, {'key': 'type', 'value': 'Frequencystamp'}]}],
                [{'labels': ['Frequency Domain Series'], 'id': 4,
                  'properties': [{'key': 'value', 'value': 'test2'}, {'key': 'type', 'value': 'Frequencystamp'}]}],
            ],
            'errors': []
        }
        frequency_domain_series_one = BasicSignalSeriesOut(id=2, type="Frequencystamp", additional_properties=[
            PropertyIn(key='value', value='test1')])
        frequency_domain_series_two = BasicSignalSeriesOut(id=4, type="Frequencystamp", additional_properties=[
            PropertyIn(key='value', value='test2')])
        frequency_domain_series_nodes = SignalSeriesNodesOut(
            signal_series_nodes=[frequency_domain_series_one, frequency_domain_series_two])
        frequency_domain_series_nodes_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()

        result = frequency_domain_series_nodes_service.get_signal_series_nodes(
            {"participant_date_of_birth": "2023-01-11"})

        self.assertEqual(frequency_domain_series_nodes, result)
        get_nodes_by_query.assert_called_once_with({
            'nodes':
                [
                    {'label': 'Frequency Domain Series', 'result': True},
                    {'label': 'Participant', 'parameters': [
                        {'key': 'date_of_birth', 'operator': 'equals',
                            'value': '2023-01-11'}
                    ]},
                    {'label': 'Participant State'},
                    {'label': 'Participation'},
                    {'label': 'Recording'},
                    {'label': 'Observable Information'}
                ],
            'relations': [
                {'begin_node_index': 0, 'end_node_index': 5,
                    'label': 'hasObservableInformation'},
                {'begin_node_index': 5, 'end_node_index': 4, 'label': 'hasRecording'},
                {'begin_node_index': 4, 'end_node_index': 3,
                    'label': 'hasParticipation'},
                {'begin_node_index': 3, 'end_node_index': 2,
                    'label': 'hasParticipantState'},
                {'begin_node_index': 2, 'end_node_index': 1,
                    'label': 'hasParticipant'}
                    ]
        })
