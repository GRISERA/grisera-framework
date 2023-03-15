import unittest
import unittest.mock as mock

from grisera_api.channel.channel_model import BasicChannelOut
from grisera_api.graph_api_service import GraphApiService
from grisera_api.recording.recording_model import BasicRecordingOut
from grisera_api.registered_channel.registered_channel_model import *
from grisera_api.registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from grisera_api.registered_data.registered_data_model import BasicRegisteredDataOut


class TestRegisteredChannelServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_registered_channel_without_errors(self, get_node_relationships_mock, get_node_mock,
                                                    create_relationships_mock, create_properties_mock,
                                                    create_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasRegisteredChannel", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 15,
             "name": "hasChannel", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 16,
             "name": "hasRegisteredData", "id": 0,
             "properties": None},
        ]}
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        registered_channel_in = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        registered_channel_out = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
                                                      recordings=[BasicRecordingOut(**{id: 19})],
                                                      channel=BasicChannelOut(**{id: 15}),
                                                      registeredData=BasicRegisteredDataOut(**{id: 16}))
        calls = [mock.call(2), mock.call(3), mock.call(1)]
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.save_registered_channel(registered_channel_in)

        self.assertEqual(result, registered_channel_out)
        create_node_mock.assert_called_once_with('`Registered Channel`')
        create_properties_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_registered_channel_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        registered_channel = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.save_registered_channel(registered_channel)

        self.assertEqual(result, RegisteredChannelOut(errors=['error']))
        create_node_mock.assert_called_once_with('`Registered Channel`')
