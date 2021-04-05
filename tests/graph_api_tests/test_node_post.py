from graph_api.node.node_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_node(*args, **kwargs):
    node_out = NodeOut(id=5, labels=args[0].labels, errors=None)
    return node_out


class TestNodePost(unittest.TestCase):

    @mock.patch.object(NodeService, 'save_node')
    def test_node_post_without_error(self, mock_service):
        mock_service.side_effect = return_node
        response = Response()
        node = NodeIn(labels={"test"})
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node(node, response))

        self.assertEqual(result, NodeOut(id=5, labels={"test"}, errors=None))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'save_node')
    def test_node_post_with_error(self, mock_service):
        mock_service.return_value = NodeOut(id=5, errors={'errors': ['test']})
        response = Response()
        node = NodeIn()
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node(node, response))

        self.assertEqual(response.status_code, 422)
