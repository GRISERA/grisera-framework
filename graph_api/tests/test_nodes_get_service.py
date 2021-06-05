from node.node_service import NodeService
from node.node_model import *
import unittest
import unittest.mock as mock
from requests import Response
import json
from node.node_model import NodeIn, NodeOut, BasicNodeOut


class TestNodesGetService(unittest.TestCase):

    @mock.patch('database_service.requests')
    def test_nodes_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [
                                        {'data':[
                                            {
                                            'row': [{}],
                                            'meta': [
                                                {'id': '5'}]

                                        }]
                                        }],
                                        'errors': []}).encode('utf-8')
        mock_requests.post.return_value = response
        label = "Test"
        node_service = NodeService()

        result = node_service.get_nodes(label)

        self.assertEqual(result, [BasicNodeOut(id=5, labels={"Test"}, properties=[])])

    @mock.patch('database_service.requests')
    def test_nodes_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [{'data': [{'meta': [{}]}]}],
                                        'errors': ['error']}).encode('utf-8')
        mock_requests.post.return_value = response
        label = "Test"
        node_service = NodeService()

        result = node_service.get_nodes(label)

        self.assertEqual(result, {'errors': ['error']})
