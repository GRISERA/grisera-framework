import unittest
from unittest import mock

from graph_api_service import GraphApiService
from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesIn, Type, SignalIn, StampNodesIn, \
    SignalValueNodesIn
from frequency_domain_series.frequency_domain_series_service_graphdb_with_signal_values import FrequencyDomainSeriesServiceGraphDBWithSignalValues


class TestFrequencyDomainSeriesWithSignalValuesServicePost(unittest.TestCase):
    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_create_signal_value_first_without_errors(self, create_relationships_mock, create_properties_mock,
                                                      create_node_mock):
        node = {'id': 50, 'properties': [], "errors": None, 'links': None}
        create_node_mock.return_value = node
        create_properties_mock.return_value = {
            'id': 50, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {
            'start_node': 40, 'end_node': 50, 'name': 'hasSignal', 'errors': None}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.create_signal_value(
            SignalValueNodesIn(value=75), None, 40)

        self.assertEqual(node, result)

        self.assertEqual([mock.call('Signal Value')],
                         create_node_mock.call_args_list)
        self.assertEqual([mock.call(50, SignalValueNodesIn(
            value=75))], create_properties_mock.call_args_list)
        self.assertEqual([mock.call(start_node=40, end_node=50, name='hasSignal')],
                         create_relationships_mock.call_args_list)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_create_signal_value_next_without_errors(self, create_relationships_mock, create_properties_mock,
                                                     create_node_mock):
        previous_signal_node = {
            'id': 10, 'properties': [], "errors": None, 'links': None}
        node = {'id': 50, 'properties': [], "errors": None, 'links': None}
        create_node_mock.return_value = node
        create_properties_mock.return_value = node
        create_relationships_mock.return_value = {
            'start_node': 10, 'end_node': 50, 'name': 'next', 'errors': None}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.create_signal_value(
            SignalValueNodesIn(value=75), previous_signal_node, 40)

        self.assertEqual(node, result)

        self.assertEqual([mock.call('Signal Value')],
                         create_node_mock.call_args_list)
        self.assertEqual([mock.call(50, SignalValueNodesIn(
            value=75))], create_properties_mock.call_args_list)
        self.assertEqual([mock.call(start_node=10, end_node=50,
                         name='next')], create_relationships_mock.call_args_list)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_get_or_create_stamp_node_first_without_errors(self, delete_relationship_mock, get_node_mock,
                                                           create_relationships_mock, create_properties_mock,
                                                           create_node_mock):
        node = {'id': 50, 'properties': [], "errors": None, 'links': None}
        get_node_mock.return_value = node
        create_node_mock.return_value = node
        create_properties_mock.return_value = node

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.get_or_create_stamp_node(
            100, None)

        self.assertEqual(node, result)

        self.assertEqual([mock.call('Frequencystamp')],
                         create_node_mock.call_args_list)
        self.assertEqual([mock.call(50, StampNodesIn(frequencystamp=100))],
                         create_properties_mock.call_args_list)
        self.assertEqual([mock.call(50)], get_node_mock.call_args_list)
        create_relationships_mock.assert_not_called()
        delete_relationship_mock.assert_not_called()

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_get_or_create_stamp_node_same_frequencystamp_without_errors(self, delete_relationship_mock, get_node_mock,
                                                                         create_relationships_mock,
                                                                         create_properties_mock,
                                                                         create_node_mock):
        previous_node = {'id': 10, 'properties': [
            {"key": "frequencystamp", "value": 100}], "errors": None, 'links': None}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.get_or_create_stamp_node(
            100, previous_node)

        self.assertEqual(previous_node, result)

        create_node_mock.assert_not_called()
        create_properties_mock.assert_not_called()
        get_node_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        delete_relationship_mock.assert_not_called()

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_get_or_create_stamp_node_smaller_frequencystamp_without_errors(self, delete_relationship_mock,
                                                                            get_node_mock, create_relationships_mock,
                                                                            create_properties_mock,
                                                                            create_node_mock):
        previous_node = {'id': 80, 'properties': [
            {"key": "frequencystamp", "value": 200}], "errors": None, 'links': None}
        node = {'id': 50, 'properties': [], "errors": None, 'links': None}
        get_node_mock.return_value = node
        create_node_mock.return_value = node
        create_properties_mock.return_value = {
            'id': 50, 'errors': None, 'links': None}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.get_or_create_stamp_node(
            100, previous_node)

        self.assertEqual(node, result)

        self.assertEqual([mock.call('Frequencystamp')],
                         create_node_mock.call_args_list)
        self.assertEqual([mock.call(50, StampNodesIn(frequencystamp=100))],
                         create_properties_mock.call_args_list)
        self.assertEqual([mock.call(50)], get_node_mock.call_args_list)
        self.assertEqual([mock.call(start_node=50, end_node=80,
                         name='next')], create_relationships_mock.call_args_list)
        delete_relationship_mock.assert_not_called()

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_get_or_create_stamp_node_greater_frequencystamp_at_the_end_without_errors(self, delete_relationship_mock,
                                                                                       get_node_relationships_mock,
                                                                                       get_node_mock,
                                                                                       create_relationships_mock,
                                                                                       create_properties_mock,
                                                                                       create_node_mock):
        previous_node = {'id': 10, 'properties': [
            {"key": "frequencystamp", "value": 75}], "errors": None, 'links': None}
        node = {'id': 50, 'properties': [], "errors": None, 'links': None}
        get_node_mock.return_value = node
        create_node_mock.return_value = node
        create_properties_mock.return_value = {
            'id': 50, 'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": []}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.get_or_create_stamp_node(
            100, previous_node)

        self.assertEqual(node, result)

        self.assertEqual([mock.call('Frequencystamp')],
                         create_node_mock.call_args_list)
        self.assertEqual([mock.call(50, StampNodesIn(frequencystamp=100))],
                         create_properties_mock.call_args_list)
        self.assertEqual([mock.call(50)], get_node_mock.call_args_list)
        self.assertEqual([mock.call(start_node=10, end_node=50,
                         name='next')], create_relationships_mock.call_args_list)
        delete_relationship_mock.assert_not_called()
        self.assertEqual(
            [mock.call(10)], get_node_relationships_mock.call_args_list)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_get_or_create_stamp_node_greater_frequencystamp_in_the_middle_without_errors(self, delete_relationship_mock,
                                                                                          get_node_relationships_mock,
                                                                                          get_node_mock,
                                                                                          create_relationships_mock,
                                                                                          create_properties_mock,
                                                                                          create_node_mock):
        previous_node = {'id': 10, 'properties': [
            {"key": "frequencystamp", "value": 75}], "errors": None, 'links': None}
        next_node = {'id': 70, 'properties': [
            {"key": "frequencystamp", "value": 125}], "errors": None, 'links': None}
        node = {'id': 50, 'properties': [], "errors": None, 'links': None}

        def get_node_side_effect(*args):
            if args[0] == 50:
                return node
            elif args[0] == 70:
                return next_node

        get_node_mock.side_effect = get_node_side_effect
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 10, "end_node": 70,
                "name": "next", "id": 15, "properties": None}
        ]}
        create_node_mock.return_value = node
        create_properties_mock.return_value = {
            'id': 50, 'errors': None, 'links': None}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.get_or_create_stamp_node(
            100, previous_node)

        self.assertEqual(node, result)

        self.assertEqual([mock.call('Frequencystamp')],
                         create_node_mock.call_args_list)
        self.assertEqual([mock.call(50, StampNodesIn(frequencystamp=100))],
                         create_properties_mock.call_args_list)

        self.assertEqual([
            mock.call(70),
            mock.call(50),
        ], get_node_mock.call_args_list)
        self.assertEqual([
            mock.call(start_node=10, end_node=50, name='next'),
            mock.call(start_node=50, end_node=70, name='next'),
        ], create_relationships_mock.call_args_list)
        self.assertEqual(
            [mock.call(15)], delete_relationship_mock.call_args_list)
        self.assertEqual(
            [mock.call(10)], get_node_relationships_mock.call_args_list)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    @mock.patch.object(FrequencyDomainSeriesServiceGraphDBWithSignalValues, 'get_or_create_stamp_node')
    @mock.patch.object(FrequencyDomainSeriesServiceGraphDBWithSignalValues, 'create_signal_value')
    def test_save_signal_values_first_without_errors(self, create_signal_value_mock, get_or_create_stamp_node_mock,
                                                     delete_relationship_mock,
                                                     get_node_relationships_mock,
                                                     get_node_mock,
                                                     create_relationships_mock,
                                                     create_properties_mock,
                                                     create_node_mock):
        get_or_create_stamp_node_mock.return_value = {'id': 60, 'properties': [{"key": "frequencystamp", "value": 100}],
                                                      "errors": None, 'links': None}
        create_signal_value_mock.return_value = {'id': 70, 'properties': [{"key": "value", "value": 10}],
                                                 "errors": None,
                                                 'links': None}

        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()
        result = frequency_domain_series_service.save_signal_values(
            [SignalIn(frequencystamp=100, signal_value=SignalValueNodesIn(value=10))], 15, 20, Type.frequencystamp)

        self.assertEqual(None, result)

        create_node_mock.assert_not_called()
        create_properties_mock.assert_not_called()
        get_node_mock.assert_not_called()
        self.assertEqual([
            mock.call(start_node=20, end_node=60, name='takes'),
            mock.call(start_node=60, end_node=70, name='inHz')
        ], create_relationships_mock.call_args_list)

        delete_relationship_mock.assert_not_called()
        self.assertEqual(
            [mock.call(20)], get_node_relationships_mock.call_args_list)
        self.assertEqual([mock.call(SignalValueNodesIn(
            value=10), None, 15)], create_signal_value_mock.call_args_list)
        self.assertEqual([mock.call(100, None)],
                         get_or_create_stamp_node_mock.call_args_list)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_signal_series_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {
            'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        frequency_domain_series = SignalSeriesIn(
            type="Frequencystamp", source="cos", observable_information_id=1, measure_id=2)
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()

        result = frequency_domain_series_service.save_signal_series(
            frequency_domain_series)

        self.assertEqual(result, SignalSeriesOut(
            type="Frequencystamp", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('Frequency Domain Series')

    @mock.patch.object(GraphApiService, 'get_nodes_by_query')
    def test_get_experiment_id_without_error(self, get_nodes_by_query_mock):
        get_nodes_by_query_mock.return_value = {
            'rows': [
                [{'labels': ['Experiment'], 'id': 23, 'properties': [
                    {'key': 'value', 'value': '10'}]}],
            ],
            'errors': []
        }
        frequency_domain_series_service = FrequencyDomainSeriesServiceGraphDBWithSignalValues()

        result = frequency_domain_series_service.get_experiment_id(10)

        self.assertEqual(23, result)
        get_nodes_by_query_mock.assert_called_once()
