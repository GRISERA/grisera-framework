import asyncio
import unittest
import unittest.mock as mock

from registered_channel.registered_channel_router import *


class TestRegisteredChannelRouterPost(unittest.TestCase):

    @mock.patch.object(RegisteredChannelService, 'save_registered_channel')
    def test_create_registered_channel_without_error(self, save_registered_channel_mock):
        save_registered_channel_mock.return_value = RegisteredChannelOut(id=1)
        response = Response()
        registered_channel = RegisteredChannelIn(channel_id=1, registered_data_id=2)
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.create_registered_channel(registered_channel, response))

        self.assertEqual(result, RegisteredChannelOut(id=1, links=get_links(router)))
        save_registered_channel_mock.assert_called_once_with(registered_channel)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredChannelService, 'save_registered_channel')
    def test_create_registered_channel_with_error(self, save_registered_channel_mock):
        save_registered_channel_mock.return_value = RegisteredChannelOut(errors={'errors': ['test']})
        response = Response()
        registered_channel = RegisteredChannelIn(channel_id=1, registered_data_id=2)
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.create_registered_channel(registered_channel, response))

        self.assertEqual(result, RegisteredChannelOut(errors={'errors': ['test']}, links=get_links(router)))
        save_registered_channel_mock.assert_called_once_with(registered_channel)
        self.assertEqual(response.status_code, 422)
