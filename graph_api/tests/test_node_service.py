from node.node_service import NodeService
from node.node_model import *
import unittest
import unittest.mock as mock
from requests import Response
import json


class TestNodePostService(unittest.TestCase):

    @mock.patch('database_service.requests')
    def test_node_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [
                                        {'data': [
                                            {'meta': [
                                                {'id': '5'}]
                                            }]
                                        }],
                                        'errors': []}).encode('utf-8')
        mock_requests.post.return_value = response
        node = NodeIn(labels={"test"})
        node_service = NodeService()

        result = node_service.save_node(node)

        self.assertEqual(result, NodeOut(id=5, labels={"test"}, errors=None))

    @mock.patch('database_service.requests')
    def test_node_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [{'data': [{'meta': [{}]}]}],
                                        'errors': ['error']}).encode('utf-8')
        mock_requests.post.return_value = response
        node = NodeIn(labels={"test"})
        node_service = NodeService()

        result = node_service.save_node(node)

        self.assertEqual(result, NodeOut(errors=['error']))
