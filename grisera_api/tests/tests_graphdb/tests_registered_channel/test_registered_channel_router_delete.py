import asyncio
import unittest
import unittest.mock as mock

from registered_channel.registered_channel_router import *
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB


class TestRegisteredChannelRouterDelete(unittest.TestCase):

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'delete_registered_channel')
    def test_delete_registered_channel_without_error(self, delete_registered_channel_mock):
        database_name = "neo4j"
        registered_channel_id = 1
        delete_registered_channel_mock.return_value = RegisteredChannelOut(id=registered_channel_id)
        response = Response()
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.delete_registered_channel(registered_channel_id, response, database_name))

        self.assertEqual(result, RegisteredChannelOut(id=registered_channel_id, links=get_links(router)))
        delete_registered_channel_mock.assert_called_once_with(registered_channel_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'delete_registered_channel')
    def test_delete_registered_channel_with_error(self, delete_registered_channel_mock):
        database_name = "neo4j"
        delete_registered_channel_mock.return_value = RegisteredChannelOut(errors={'errors': ['test']})
        response = Response()
        registered_channel_id = 1
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.delete_registered_channel(registered_channel_id, response, database_name))

        self.assertEqual(result, RegisteredChannelOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_registered_channel_mock.assert_called_once_with(registered_channel_id, database_name)
        self.assertEqual(response.status_code, 404)
