import json
import unittest
import unittest.mock as mock
from registered_channel.registered_channel_model import *
from registered_channel.registered_channel_service import RegisteredChannelService
from requests import Response


class TestRegisteredChannelPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_registered_channel_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 2, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        get_response = Response()
        get_response._content = json.dumps({'nodes': [{'id': 1, 'properties': [{'key': 'type', 'value': 'ECG'}]}],
                                            'errors': None,
                                            'links': []}).encode('utf-8')
        mock_requests.get.return_value = get_response
        registered_channel = RegisteredChannelIn(channel="ECG", registered_data_id=1)
        registered_channel_service = RegisteredChannelService()

        result = registered_channel_service.save_registered_channel(registered_channel)

        self.assertEqual(result, RegisteredChannelOut(channel="ECG", registered_data_id=1, id=2))

    @mock.patch('graph_api_service.requests')
    def test_registered_channel_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        registered_channel = RegisteredChannelIn(channel="ECG", registered_data_id=1)
        registered_channel_service = RegisteredChannelService()

        result = registered_channel_service.save_registered_channel(registered_channel)

        self.assertEqual(result, RegisteredChannelOut(channel="ECG", registered_data_id=1,
                                                      errors={'error': 'test'}))
