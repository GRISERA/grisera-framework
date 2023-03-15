import asyncio
import unittest
import unittest.mock as mock

from grisera_api.registered_channel.registered_channel_router import *
from grisera_api.registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB


class TestRegisteredChannelRouterPut(unittest.TestCase):

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'update_registered_channel_relationships')
    def test_update_registered_channel_relationships_without_error(self, update_registered_channel_relationships_mock):
        id_node = 1
        update_registered_channel_relationships_mock.return_value = RegisteredChannelOut(id=id_node)
        response = Response()
        registered_channel_in = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        registered_channel_out = RegisteredChannelOut(id=id_node, links=get_links(router))
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.
                             update_registered_channel_relationships(id_node, registered_channel_in, response))

        self.assertEqual(result, registered_channel_out)
        update_registered_channel_relationships_mock.assert_called_once_with(id_node, registered_channel_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredChannelServiceGraphDB, 'update_registered_channel_relationships')
    def test_update_registered_channel_relationships_with_error(self, update_registered_channel_relationships_mock):
        id_node = 1
        update_registered_channel_relationships_mock.return_value = RegisteredChannelOut(id=id_node, errors="error")
        response = Response()
        registered_channel_in = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        registered_channel_out = RegisteredChannelOut(id=id_node, errors="error", links=get_links(router))
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.
                             update_registered_channel_relationships(id_node, registered_channel_in, response))

        self.assertEqual(result, registered_channel_out)
        update_registered_channel_relationships_mock.assert_called_once_with(id_node, registered_channel_in)
        self.assertEqual(response.status_code, 404)
