import json
import unittest
import unittest.mock as mock
from channel.channel_model import *
from channel.channel_service import ChannelService
from requests import Response


class TestChannelPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_channel_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        channel = ChannelIn(type="ECG")
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(type="ECG", id=1))

    @mock.patch('graph_api_service.requests')
    def test_channel_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        channel = ChannelIn(type="ECG")
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(type="ECG", errors={'error': 'test'}))
