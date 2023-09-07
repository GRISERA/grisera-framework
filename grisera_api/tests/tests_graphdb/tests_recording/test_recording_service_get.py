import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from models.not_found_model import *
from observable_information.observable_information_model import BasicObservableInformationOut
from participation.participation_model import BasicParticipationOut
from recording.recording_model import *
from recording.recording_service_graphdb import RecordingServiceGraphDB
from property.property_model import *
from registered_channel.registered_channel_model import BasicRegisteredChannelOut


class TestRecordingServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_recording_without_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Recording'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        recording = BasicRecordingOut(additional_properties=[], id=id_node)
        recording_service = RecordingServiceGraphDB()

        result = recording_service.get_recording(id_node, dataset_name)

        self.assertEqual(result, recording)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_recording_without_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        recording_service = RecordingServiceGraphDB()

        result = recording_service.get_recording(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_recording_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        recording_service = RecordingServiceGraphDB()

        result = recording_service.get_recording(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_recordings(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Recording'],
                                                  'properties': [{'key': 'test', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Recording'],
                                                  'properties': [{'key': 'test2', 'value': 'test3'}]}]}
        recording_one = BasicRecordingOut(additional_properties=[PropertyIn(key='test', value='test')],
                                          id=1)
        recording_two = BasicRecordingOut(additional_properties=[PropertyIn(key='test2', value='test3')],
                                          id=2)
        recordings = RecordingsOut(
            recordings=[recording_one, recording_two])
        recordings_service = RecordingServiceGraphDB()

        result = recordings_service.get_recordings(dataset_name)

        self.assertEqual(result, recordings)
        get_nodes_mock.assert_called_once_with("Recording", dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_recordings_empty(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': []}
        recordings = RecordingsOut(recording=[])
        recordings_service = RecordingServiceGraphDB()

        result = recordings_service.get_recordings(dataset_name)

        self.assertEqual(result, recordings)
        get_nodes_mock.assert_called_once_with("Recording", dataset_name)
