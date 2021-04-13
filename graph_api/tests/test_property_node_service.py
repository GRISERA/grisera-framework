from node.node_service import NodeService
from node.node_model import *
import unittest
import unittest.mock as mock
from requests import Response
import json


class TestPropertyNodePostService(unittest.TestCase):

    @mock.patch('database_service.requests')
    def test_property_node_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [
            {'data': [
                {'row': [
                    ["test"],
                    {'testkey': 'testvalue'}
                ]
                }
            ]
            }
        ],
            'errors': []}).encode('utf-8')
        mock_requests.post.return_value = response
        node_service = NodeService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = node_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, NodeOut(labels={"test"}, id=5, properties=properties))

    @mock.patch('database_service.requests')
    def test_property_node_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [{'data': [{'meta': [{}]}]}],
                                        'errors': ['error']}).encode('utf-8')
        mock_requests.post.return_value = response
        node_service = NodeService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = node_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, NodeOut(errors=['error']))
