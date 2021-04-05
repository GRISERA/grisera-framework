from graph_api.node.node_service import NodeService
from graph_api.node.node_model import *
import unittest
import unittest.mock as mock
from requests import Response


class TestNodePostService(unittest.TestCase):

    @mock.patch.object(Response, 'json')
    def test_node_service_without_error(self, mock_requests):
        mock_requests.return_value = {'results': [
                                                {'data': [
                                                    {'meta': [
                                                        {'id': '5'}]
                                                    }]
                                                }],
                                      'errors': []}
        node = NodeIn(labels={"test"})
        node_service = NodeService()

        result = node_service.save_node(node)

        self.assertEqual(result, NodeOut(id=5, labels={"test"}, errors=None))

    @mock.patch.object(Response, 'json')
    def test_node_service_with_error(self, mock_requests):
        mock_requests.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                      'errors': ['error']}
        node = NodeIn(labels={"test"})
        node_service = NodeService()

        result = node_service.save_node(node)

        self.assertEqual(result, NodeOut(errors=['error']))
