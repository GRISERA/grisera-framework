import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from recording.recording_model import *
from recording.recording_service_graphdb import RecordingServiceGraphDB


class TestRecordingServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_recording_without_errors(self, get_node_relationships_mock, get_node_mock,
                                                    create_relationships_mock, create_properties_mock,
                                                    create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Recording'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        additional_properties = []
        recording_in = RecordingIn(participation_id=2, registered_channel_id=3)
        recording_out = RecordingOut(additional_properties=additional_properties, relations=
                                                      [RelationInformation(second_node_id=19, name="testRelation",
                                                                           relation_id=0)],
                                                      reversed_relations=
                                                      [RelationInformation(second_node_id=15,
                                                                           name="testReversedRelation",
                                                                           relation_id=0)], id=id_node)
        calls = [mock.call(2, dataset_name), mock.call(3, dataset_name), mock.call(1, dataset_name)]
        recording_service = RecordingServiceGraphDB()

        result = recording_service.save_recording(recording_in, dataset_name)

        self.assertEqual(result, recording_out)
        create_node_mock.assert_called_once_with('Recording', dataset_name)
        # create_properties_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_recording_with_node_error(self, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        recording = RecordingIn()
        recording_service = RecordingServiceGraphDB()

        result = recording_service.save_recording(recording, dataset_name)

        self.assertEqual(result, RecordingOut(errors=['error']))
        create_node_mock.assert_called_once_with('Recording', dataset_name)

