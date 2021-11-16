import asyncio
import unittest
import unittest.mock as mock

from registered_channel.registered_channel_router import *


class TestRegisteredChannelRouterDelete(unittest.TestCase):

    @mock.patch.object(RegisteredChannelService, 'delete_registered_channel')
    def test_delete_registered_channel_without_error(self, delete_registered_channel_mock):
        registered_channel_id = 1
        delete_registered_channel_mock.return_value = RegisteredChannelOut(id=registered_channel_id)
        response = Response()
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.delete_registered_channel(registered_channel_id, response))

        self.assertEqual(result, RegisteredChannelOut(id=registered_channel_id, links=get_links(router)))
        delete_registered_channel_mock.assert_called_once_with(registered_channel_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredChannelService, 'delete_registered_channel')
    def test_delete_registered_channel_with_error(self, delete_registered_channel_mock):
        delete_registered_channel_mock.return_value = RegisteredChannelOut(errors={'errors': ['test']})
        response = Response()
        registered_channel_id = 1
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.delete_registered_channel(registered_channel_id, response))

        self.assertEqual(result, RegisteredChannelOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_registered_channel_mock.assert_called_once_with(registered_channel_id)
        self.assertEqual(response.status_code, 404)
