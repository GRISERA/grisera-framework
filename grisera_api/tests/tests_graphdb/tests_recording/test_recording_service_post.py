import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from observable_information.observable_information_model import BasicObservableInformationOut
from participation.participation_model import BasicParticipationOut
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from recording.recording_model import *
from recording.recording_service_graphdb import RecordingServiceGraphDB
from registered_channel.registered_channel_model import BasicRegisteredChannelOut
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB


class TestRecordingServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(ParticipationServiceGraphDB, 'get_participation')
    @mock.patch.object(RegisteredChannelServiceGraphDB, 'get_registered_channel')
    def test_save_recording_without_errors(self, get_registered_channel_mock, get_participation_mock,
                                           get_node_mock,
                                           create_relationships_mock, create_properties_mock,
                                           create_node_mock):
        dataset_name = "neo4j"
        id_node = 1

        create_node_mock.return_value = {'id': id_node, 'labels': ['Recording'],
                                         'properties': [],
                                         "errors": None, 'links': None}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Recording'],
                                      "errors": None, 'links': None, 'properties': [{'key': 'identifier', 'value': 5}]}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        recording_out = BasicRecordingOut(id=id_node, additional_properties=additional_properties)
        recording_in = RecordingIn(participation_id=6, registered_channel_id=7,
                                   additional_properties=additional_properties)

        recording_service = RecordingServiceGraphDB()

        recording_service.participation_service = mock.create_autospec(ParticipationServiceGraphDB)
        get_participation_mock.return_value = BasicParticipationOut(id=6)
        recording_service.participation_service.get_participation = get_participation_mock

        recording_service.registered_channel_service = mock.create_autospec(RegisteredChannelServiceGraphDB)
        get_registered_channel_mock.return_value = BasicRegisteredChannelOut(id=7, additional_properties=additional_properties)
        recording_service.registered_channel_service.get_registered_channel = get_registered_channel_mock

        result = recording_service.save_recording(recording_in, dataset_name)


        create_relationships_mock.assert_has_calls(
            [mock.call(start_node=id_node, end_node=6,name="hasParticipation"),
             mock.call(start_node=id_node, end_node=7, name="hasRegisteredChannel")])
        create_properties_mock.assert_called_once_with(id_node, recording_in)
        get_node_mock.assert_called_once_with(id_node)
        self.assertEqual(result, recording_out)

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
