import unittest
import unittest.mock as mock

from channel.channel_model import *
from channel.channel_service import ChannelService
from graph_api_service import GraphApiService
from models.not_found_model import *


class TestChannelServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_channel_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Channel'],
                                      'properties': [{'key': 'type', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        channel = ChannelOut(type="test", id=id_node,
                             relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                            relation_id=0)],
                             reversed_relations=[RelationInformation(second_node_id=15,
                                                                     name="testReversedRelation", relation_id=0)])
        channel_service = ChannelService()

        result = channel_service.get_channel(id_node)

        self.assertEqual(result, channel)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_channel_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        channel_service = ChannelService()

        result = channel_service.get_channel(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_channel_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        channel_service = ChannelService()

        result = channel_service.get_channel(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_channels(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Channel'],
                                                  'properties': [{'key': 'type', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Channel'],
                                                  'properties': [{'key': 'type', 'value': 'test2'}]}],
                                       'errors': None}
        channel_one = BasicChannelOut(type="test", id=1)
        channel_two = BasicChannelOut(type="test2", id=2)
        channels = ChannelsOut(channels=[channel_one, channel_two])
        channel_service = ChannelService()

        result = channel_service.get_channels()

        self.assertEqual(result, channels)
        get_nodes_mock.assert_called_once_with("Channel")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_channels_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        channels = ChannelsOut(channels=[])
        channel_service = ChannelService()

        result = channel_service.get_channels()

        self.assertEqual(result, channels)
        get_nodes_mock.assert_called_once_with("Channel")
