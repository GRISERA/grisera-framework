from node.node_router import *
import unittest
import unittest.mock as mock
import asyncio
from node.node_model import NodeIn, NodeOut, BasicNodeOut, NodesOut


def return_nodes(*args, **kwargs):
    nodes_out = NodesOut(nodes=[BasicNodeOut(id=5, labels={args[0]})])
    return nodes_out


class TestNodesGet(unittest.TestCase):

    @mock.patch.object(NodeService, 'get_nodes')
    def test_nodes_get_without_error(self, mock_service):
        mock_service.side_effect = return_nodes
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_nodes(label, response))

        self.assertEqual(result, NodesOut(nodes=[BasicNodeOut(id=5, labels={label})], links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'get_nodes')
    def test_nodes_get_with_error(self, mock_service):
        mock_service.return_value = NodesOut(errors='error')
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_nodes(label, response))

        self.assertEqual(response.status_code, 422)
