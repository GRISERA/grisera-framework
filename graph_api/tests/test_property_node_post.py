from node.node_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_node(*args, **kwargs):
    node_out = NodeOut(id=5, properties=args[1], errors=None)
    return node_out


class TestNodePost(unittest.TestCase):

    @mock.patch.object(NodeService, 'save_properties')
    def test_properties_for_node_post_without_error(self, mock_service):
        mock_service.side_effect = return_node
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node_properties(id, properties, response))

        self.assertEqual(result, NodeOut(id=5, properties=properties, errors=None, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'save_properties')
    def test_properties_for_node_post_with_error(self, mock_service):
        mock_service.return_value = NodeOut(id=5, errors={'errors': ['test']})
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node_properties(id, properties, response))

        self.assertEqual(response.status_code, 422)
