import asyncio
import unittest
import unittest.mock as mock

from channel.channel_model import BasicChannelOut
from channel.channel_router import *
from channel.channel_service_graphdb import ChannelServiceGraphDB


class TestChannelRouterGet(unittest.TestCase):

    @mock.patch.object(ChannelServiceGraphDB, 'get_channel')
    def test_get_channel_without_error(self, get_channel_mock):
        channel_id = 1
        get_channel_mock.return_value = ChannelOut(type='url', id=channel_id)
        response = Response()
        channel_router = ChannelRouter()

        result = asyncio.run(channel_router.get_channel(channel_id, response))

        self.assertEqual(result, ChannelOut(type='url', id=channel_id, links=get_links(router)))
        get_channel_mock.assert_called_once_with(channel_id, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ChannelServiceGraphDB, 'get_channel')
    def test_get_channel_with_error(self, get_channel_mock):
        get_channel_mock.return_value = ChannelOut(type='url', errors={'errors': ['test']})
        response = Response()
        channel_id = 1
        channel_router = ChannelRouter()

        result = asyncio.run(channel_router.get_channel(channel_id, response))

        self.assertEqual(result, ChannelOut(type='url', errors={'errors': ['test']}, links=get_links(router)))
        get_channel_mock.assert_called_once_with(channel_id, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ChannelServiceGraphDB, 'get_channels')
    def test_get_channel_nodes_without_error(self, get_channels_mock):
        get_channels_mock.return_value = ChannelsOut(channels=[
            BasicChannelOut(type='url', id=1), BasicChannelOut(type='url2', id=2)])
        response = Response()
        channel_router = ChannelRouter()

        result = asyncio.run(channel_router.get_channels(response))

        self.assertEqual(result, ChannelsOut(channels=[
            BasicChannelOut(type='url', id=1), BasicChannelOut(type='url2', id=2)],
            links=get_links(router)))
        get_channels_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
