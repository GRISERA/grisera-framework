import unittest
import unittest.mock as mock

from observable_information.observable_information_model import BasicObservableInformationOut
from participation.participation_model import BasicParticipationOut
from recording.recording_model import *
from models.not_found_model import *

from recording.recording_service_graphdb import RecordingServiceGraphDB
from graph_api_service import GraphApiService
from registered_channel.registered_channel_model import BasicRegisteredChannelOut


class TestRecordingServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    def test_update_recording_without_error(self, delete_node_properties_mock,
                                            get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Recording'],
                                      'properties': [{'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        recording_in = RecordingPropertyIn(id=id_node, additional_properties=additional_properties)
        recording_out = BasicRecordingOut(additional_properties=additional_properties, id=id_node)
        calls = [mock.call(1)]
        recording_service = RecordingServiceGraphDB()

        result = recording_service.update_recording(id_node, recording_in)

        self.assertEqual(result, recording_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_called_once_with(id_node, recording_in)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_recording_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        additional_properties = [PropertyIn(key='identifier', value=5)]
        recording_in = RecordingPropertyIn(id=id_node, additional_properties=additional_properties)
        recording_service = RecordingServiceGraphDB()

        result = recording_service.update_recording(id_node, recording_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_recording_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        additional_properties = [PropertyIn(key='identifier', value=5)]
        recording_in = RecordingPropertyIn(id=id_node, additional_properties=additional_properties)
        recording_service = RecordingServiceGraphDB()

        result = recording_service.update_recording(id_node, recording_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
