import unittest
import unittest.mock as mock

from activity.activity_model import *
from graph_api_service import GraphApiService
from recording.recording_model import *
from recording.recording_service import RecordingService


class TestRecordingService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_recording_without_error(self, create_properties_mock, create_relationships_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_relationships_mock.return_value = {'id': 4, 'name': 'has', 'start_node': 2, 'end_node': 3,
                                                  "errors": None, 'links': None}
        create_properties_mock.return_value = {'errors': None}
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_service = RecordingService()
        calls = [mock.call(id_node, 2, 'hasRegisteredChannel'), mock.call(id_node, 3, 'hasParticipation')]

        result = recording_service.save_recording(recording)

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=id_node))
        create_node_mock.assert_called_once_with('Recording')
        create_relationships_mock.assert_has_calls(calls)
        create_properties_mock.assert_called_once_with(id_node, recording)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_recording_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_service = RecordingService()

        result = recording_service.save_recording(recording)

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, errors=['error']))
        create_node_mock.assert_called_once_with('Recording')
