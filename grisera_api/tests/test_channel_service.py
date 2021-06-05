import json
import unittest
import unittest.mock as mock
from channel.channel_model import *
from channel.channel_service import ChannelService
from requests import Response


class TestChannelPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_channel_post_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        channel = ChannelIn(type="ECG")
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(type="ECG", id=1))

    @mock.patch('graph_api_service.requests')
    def test_channel_post_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        channel = ChannelIn(type="ECG")
        channel_service = ChannelService()

        result = channel_service.save_channel(channel)

        self.assertEqual(result, ChannelOut(type="ECG", errors={'error': 'test'}))

    @mock.patch('graph_api_service.requests')
    def test_channel_get_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'Channel': [{'id': 1, 'properties': [{'key': 'type', 'value': 'ECG'}]}],
                                        'links': []}).encode('utf-8')
        mock_requests.get.return_value = response
        channel_service = ChannelService()

        result = channel_service.get_channels()

        self.assertEqual(result, ChannelsOut(channels=[BasicChannelOut(id=1, type='ECG')]))

    @mock.patch('graph_api_service.requests')
    def test_channel_get_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'Channel': {'errors': 'error'},
                                        'links': []}).encode('utf-8')
        mock_requests.get.return_value = response
        channel_service = ChannelService()

        result = channel_service.get_channels()

        self.assertEqual(result, ChannelsOut(errors={'errors': 'error'}))
