import json
import unittest
import unittest.mock as mock
from registered_data.registered_data_model import *
from registered_data.registered_data_service import RegisteredDataService
from requests import Response


class TestRegisteredDataPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_registered_data_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        registered_data = RegisteredDataIn(source="http://localhost")
        registered_data_service = RegisteredDataService()

        result = registered_data_service.save_registered_data(registered_data)

        self.assertEqual(result, RegisteredDataOut(source="http://localhost", id=1))

    @mock.patch('graph_api_service.requests')
    def test_registered_data_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        registered_data = RegisteredDataIn(source="http://localhost")
        registered_data_service = RegisteredDataService()

        result = registered_data_service.save_registered_data(registered_data)

        self.assertEqual(result, RegisteredDataOut(source="http://localhost", errors={'error': 'test'}))
