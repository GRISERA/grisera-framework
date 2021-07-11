import unittest
import unittest.mock as mock
from registered_channel.registered_channel_model import *
from registered_channel.registered_channel_service import RegisteredChannelService
from graph_api_service import GraphApiService
from channel.channel_model import ChannelsOut, BasicChannelOut
from channel.channel_service import ChannelService


class TestRegisteredChannelService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ChannelService, 'get_channels')
    def test_save_registered_channel_without_error(self, get_channels_mock, create_relationships_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_relationships_mock.return_value = {'id': 3, 'start_node': 2, "errors": None, 'links': None}
        get_channels_mock.return_value = ChannelsOut(channels=[BasicChannelOut(id=5, type="ECG")])
        calls = [mock.call(start_node=id_node, end_node=5, name="hasChannel"),
                 mock.call(start_node=id_node, end_node=1, name="hasRegisteredData")]
        registered_channel = RegisteredChannelIn(channel="ECG", registered_data_id=1)
        registered_channel_service = RegisteredChannelService()

        result = registered_channel_service.save_registered_channel(registered_channel)

        self.assertEqual(result, RegisteredChannelOut(channel="ECG", registered_data_id=1, id=id_node))
        create_node_mock.assert_called_once_with('`Registered channel`')
        get_channels_mock.assert_called_once()
        create_relationships_mock.assert_has_calls(calls)


    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_registered_channel_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        registered_channel = RegisteredChannelIn(channel="ECG", registered_data_id=1)
        registered_channel_service = RegisteredChannelService()

        result = registered_channel_service.save_registered_channel(registered_channel)

        self.assertEqual(result, RegisteredChannelOut(channel="ECG", registered_data_id=1, errors=['error']))
        create_node_mock.assert_called_once_with('`Registered channel`')
