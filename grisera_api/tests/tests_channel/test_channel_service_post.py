import unittest
import unittest.mock as mock

from channel.channel_model import *
from channel.channel_service import ChannelService
from graph_api_service import GraphApiService


class TestChannelServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_channel_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'type', 'value': 'Audio'}],
                                               "errors": None, 'links': None}
        channel = ChannelIn(type='Audio')
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(id=id_node, type='Audio'))
        create_node_mock.assert_called_once_with('Channel')
        create_properties_mock.assert_called_once_with(id_node, channel)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_channel_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        channel = ChannelIn(type='Audio')
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(type='Audio', errors=['error']))
        create_node_mock.assert_called_once_with('Channel')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_channel_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        channel = ChannelIn(type='Audio')
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(type='Audio', errors=['error']))
        create_node_mock.assert_called_once_with('Channel')
        create_properties_mock.assert_called_once_with(id_node, channel)
