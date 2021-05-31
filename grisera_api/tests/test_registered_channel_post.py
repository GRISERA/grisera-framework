from registered_channel.registered_channel_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_registered_channel(*args, **kwargs):
    registered_channel_out = RegisteredChannelOut(channel_id=0, registered_data_id=1, id=2)
    return registered_channel_out


class TestRegisteredChannelPost(unittest.TestCase):

    @mock.patch.object(RegisteredChannelService, 'save_registered_channel')
    def test_registered_channel_post_without_error(self, mock_service):
        mock_service.side_effect = return_registered_channel
        response = Response()
        registered_channel = RegisteredChannelIn(channel_id=0, registered_data_id=1)
        registered_channel_router = RegisteredChannelRouter()

        result = asyncio.run(registered_channel_router.create_registered_channel(registered_channel, response))

        self.assertEqual(result, RegisteredChannelOut(channel_id=0, registered_data_id=1,
                                                      id=2, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredChannelService, 'save_registered_channel')
    def test_registered_channel_post_with_error(self, mock_service):
        mock_service.return_value = RegisteredChannelOut(channel_id=0, registered_data_id=1, errors={'errors': ['test']})
        response = Response()
        registered_channel = RegisteredChannelIn(channel_id=0, registered_data_id=1)
        registered_channel_router = RegisteredChannelRouter()
        
        result = asyncio.run(registered_channel_router.create_registered_channel(registered_channel, response))

        self.assertEqual(response.status_code, 422)
