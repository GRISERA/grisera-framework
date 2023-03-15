import unittest
import unittest.mock as mock

from grisera_api.channel.channel_model import BasicChannelOut
from grisera_api.graph_api_service import GraphApiService
from grisera_api.models.not_found_model import *
from grisera_api.recording.recording_model import BasicRecordingOut
from grisera_api.registered_channel.registered_channel_model import *
from grisera_api.registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from grisera_api.registered_data.registered_data_model import BasicRegisteredDataOut


class TestRegisteredChannelServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_registered_channel_without_error(self, get_node_relationships_mock, get_node_mock):
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
        registered_channel = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
                                                  recordings=[BasicRecordingOut(**{id: 19})],
                                                  channel=BasicChannelOut(**{id: 15}),
                                                  registeredData=BasicRegisteredDataOut(**{id: 16}))
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.get_registered_channel(id_node)

        self.assertEqual(result, registered_channel)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_registered_channel_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.get_registered_channel(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_registered_channel_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.get_registered_channel(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_registered_channels(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Registered Channel'],
                                                  'properties': [{'key': 'age', 'value': 5},
                                                                 {'key': 'test', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Registered Channel'],
                                                  'properties': [{'key': 'age', 'value': 10},
                                                                 {'key': 'test2', 'value': 'test3'}]}]}
        registered_channel_one = BasicRegisteredChannelOut(id=1)
        registered_channel_two = BasicRegisteredChannelOut(id=2)
        registered_channels = RegisteredChannelsOut(
            registered_channels=[registered_channel_one, registered_channel_two])
        registered_channels_service = RegisteredChannelServiceGraphDB()

        result = registered_channels_service.get_registered_channels()

        self.assertEqual(result, registered_channels)
        get_nodes_mock.assert_called_once_with("`Registered Channel`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_registered_channels_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        registered_channels = RegisteredChannelsOut(registered_channel=[])
        registered_channels_service = RegisteredChannelServiceGraphDB()

        result = registered_channels_service.get_registered_channels()

        self.assertEqual(result, registered_channels)
        get_nodes_mock.assert_called_once_with("`Registered Channel`")
