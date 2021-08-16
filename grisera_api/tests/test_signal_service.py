import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from signal_node.signal_model import *
from signal_node.signal_service import SignalService


class TestSignalService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_signal_without_errors(self, create_relationships_mock, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node,
                                               'properties': [{'key': 'type', 'value': 'Epoch'},
                                                              {'key': 'source', 'value': 'cos'}],
                                               "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]
        calls = [mock.call(1, 3, 'hasObservableInformation'), mock.call(1, 4, 'hasRecording')]

        signal = SignalIn(type="Epoch", source="cos", observable_information_id=3, recording_id=4,
                          additional_properties=additional_properties)

        signal_service = SignalService()

        result = signal_service.save_signal(signal)

        self.assertEqual(result, SignalOut(type="Epoch", source="cos", observable_information_id=3, recording_id=4,
                                           id=1, additional_properties=additional_properties))

        create_node_mock.assert_called_once_with('Signal')
        create_properties_mock.assert_called_once_with(id_node, signal)
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_signal_with_signal_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        signal = SignalIn(type="Epoch", source="cos")
        signal_service = SignalService()

        result = signal_service.save_signal(signal)

        self.assertEqual(result, SignalOut(type="Epoch", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('Signal')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_signal_with_signal_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        signal = SignalIn(type="Epoch", source="cos")
        signal_service = SignalService()

        result = signal_service.save_signal(signal)

        self.assertEqual(result, SignalOut(type="Epoch", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('Signal')
        create_properties_mock.assert_called_once_with(id_node, signal)
