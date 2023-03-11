import asyncio
import unittest
import unittest.mock as mock

from registered_channel.registered_channel_model import *
from registered_channel.registered_channel_router import *
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB


class TestRegisteredChannelRouterGet(unittest.TestCase):

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'get_registered_channel')
    def test_get_registered_channel_without_error(self, get_registered_channel_mock):
        database_name = "neo4j"
        registered_channel_id = 1
        get_registered_channel_mock.return_value = RegisteredChannelOut(id=registered_channel_id)
        response = Response()
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.get_registered_channel(registered_channel_id, response, database_name))

        self.assertEqual(result, RegisteredChannelOut(id=registered_channel_id, links=get_links(router)))
        get_registered_channel_mock.assert_called_once_with(registered_channel_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'get_registered_channel')
    def test_get_registered_channel_with_error(self, get_registered_channel_mock):
        database_name = "neo4j"
        get_registered_channel_mock.return_value = RegisteredChannelOut(errors={'errors': ['test']})
        response = Response()
        registered_channel_id = 1
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.get_registered_channel(registered_channel_id, response, database_name))

        self.assertEqual(result, RegisteredChannelOut(errors={'errors': ['test']},
                                                      links=get_links(router)))
        get_registered_channel_mock.assert_called_once_with(registered_channel_id, database_name)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'get_registered_channels')
    def test_get_registered_channels_without_error(self, get_registered_channels_mock):
        database_name = "neo4j"
        get_registered_channels_mock.return_value = RegisteredChannelsOut(registered_channels=[
            BasicRegisteredChannelOut(id=1),
            BasicRegisteredChannelOut(id=2)])
        response = Response()
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.get_registered_channels(response, database_name))

        self.assertEqual(result, RegisteredChannelsOut(registered_channels=[
            BasicRegisteredChannelOut(id=1),
            BasicRegisteredChannelOut(id=2)],
            links=get_links(router)))
        get_registered_channels_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
