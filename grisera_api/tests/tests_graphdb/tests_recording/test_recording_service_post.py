import unittest
import unittest.mock as mock

from grisera_api.graph_api_service import GraphApiService
from grisera_api.observable_information.observable_information_model import BasicObservableInformationOut
from grisera_api.participation.participation_model import BasicParticipationOut
from grisera_api.recording.recording_model import *
from grisera_api.recording.recording_service_graphdb import RecordingServiceGraphDB
from grisera_api.registered_channel.registered_channel_model import BasicRegisteredChannelOut


class TestRecordingServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_recording_without_errors(self, get_node_relationships_mock, get_node_mock,
                                           create_relationships_mock, create_properties_mock,
                                           create_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Recording'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "hasRegisteredChannel", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 15,
             "name": "hasParticipation", "id": 0,
             "properties": None},
            {"start_node": 16, "end_node": id_node,
             "name": "hasRecording", "id": 0,
             "properties": None}
        ]}
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        recording_in = RecordingIn(participation_id=2, registered_channel_id=3)
        recording_out = RecordingOut(additional_properties=[], id=id_node,
                                     registered_channel=BasicRegisteredChannelOut(**{id: 19}),
                                     participation=BasicParticipationOut(**{id: 15}),
                                     observable_informations=[BasicObservableInformationOut(**{id: 16})])
        calls = [mock.call(2), mock.call(3), mock.call(1)]
        recording_service = RecordingServiceGraphDB()

        result = recording_service.save_recording(recording_in)

        self.assertEqual(result, recording_out)
        create_node_mock.assert_called_once_with('Recording')
        # create_properties_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_recording_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        recording = RecordingIn()
        recording_service = RecordingServiceGraphDB()

        result = recording_service.save_recording(recording)

        self.assertEqual(result, RecordingOut(errors=['error']))
        create_node_mock.assert_called_once_with('Recording')
