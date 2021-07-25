import asyncio
import unittest
import unittest.mock as mock

from node.node_model import *
from node.node_router import *
from relationship.relationship_model import BasicRelationshipOut


def return_new_node(*args, **kwargs):
    return NodeOut(id=5, labels=args[0].labels, errors=None)


def return_node_with_properties(*args, **kwargs):
    return NodeOut(labels={"test"}, id=5, properties=args[1], errors=None)


def return_node(*args, **kwargs):
    return NodeOut(id=args[0], labels={"Test"}, errors=None)


def return_nodes(*args, **kwargs):
    return NodesOut(nodes=[BasicNodeOut(id=5, labels={args[0]})])

def return_relationships(*args, **kwargs):
    return RelationshipsOut(relationships=[BasicRelationshipOut(id=5), BasicRelationshipOut(id=6)])



class NodeRouterTestCase(unittest.TestCase):

    @mock.patch.object(NodeService, 'save_node')
    def test_create_node_without_error(self, save_node_mock):
        save_node_mock.side_effect = return_new_node
        response = Response()
        node = NodeIn(labels={"test"})
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node(node, response))

        self.assertEqual(result, NodeOut(id=5, labels={"test"}, links=get_links(router)))
        save_node_mock.assert_called_with(node)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'save_node')
    def test_create_node_with_error(self, save_node_mock):
        save_node_mock.return_value = NodeOut(errors={'errors': ['test']})
        response = Response()
        node = NodeIn()
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node(node, response))

        self.assertEqual(result, NodeOut(errors={'errors': ['test']}, links=get_links(router)))
        save_node_mock.assert_called_with(node)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(NodeService, 'get_node')
    def test_get_node_without_error(self, get_node_mock):
        get_node_mock.side_effect = return_node
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_node(5, response))

        self.assertEqual(result, NodeOut(id=5, labels={label}, links=get_links(router)))
        get_node_mock.assert_called_with(5)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'get_node')
    def test_get_node_with_error(self, get_node_mock):
        get_node_mock.return_value = NodeOut(errors='error')
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_node(5, response))

        self.assertEqual(result, NodeOut(errors='error', links=get_links(router)))
        get_node_mock.assert_called_with(5)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(NodeService, 'delete_node')
    def test_delete_node_without_error(self, delete_node_mock):
        delete_node_mock.side_effect = return_node
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.delete_node(5, response))

        self.assertEqual(result, NodeOut(id=5, labels={label}, links=get_links(router)))
        delete_node_mock.assert_called_with(5)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'delete_node')
    def test_delete_node_with_error(self, delete_node_mock):
        delete_node_mock.return_value = NodeOut(errors='error')
        response = Response()
        node_router = NodeRouter()

        result = asyncio.run(node_router.delete_node(5, response))

        self.assertEqual(result, NodeOut(errors='error', links=get_links(router)))
        delete_node_mock.assert_called_with(5)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(NodeService, 'get_nodes')
    def test_get_nodes_without_error(self, get_nodes_mock):
        get_nodes_mock.side_effect = return_nodes
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_nodes(label, response))

        self.assertEqual(result, NodesOut(nodes=[BasicNodeOut(id=5, labels={label})], links=get_links(router)))
        get_nodes_mock.assert_called_with(label)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'get_nodes')
    def test_get_nodes_with_error(self, get_nodes_mock):
        get_nodes_mock.return_value = NodesOut(errors='error')
        response = Response()
        label = "Test"
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_nodes(label, response))

        self.assertEqual(result, NodesOut(errors='error', links=get_links(router)))
        get_nodes_mock.assert_called_with(label)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(NodeService, 'save_properties')
    def test_create_node_properties_without_error(self, save_properties_mock):
        save_properties_mock.side_effect = return_node_with_properties
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node_properties(id, properties, response))

        self.assertEqual(result, NodeOut(labels={"test"}, id=id, properties=properties, links=get_links(router)))
        save_properties_mock.assert_called_with(id, properties)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'save_properties')
    def test_create_node_properties_post_with_error(self, save_properties_mock):
        save_properties_mock.return_value = NodeOut(id=5, errors={'errors': ['test']})
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = NodeRouter()

        result = asyncio.run(node_router.create_node_properties(id, properties, response))

        self.assertEqual(result, NodeOut(id=5, errors={'errors': ['test']}, links=get_links(router)))
        save_properties_mock.assert_called_with(id, properties)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(NodeService, 'get_relationships')
    def test_get_node_relationships_without_error(self, get_relationships_mock):
        get_relationships_mock.side_effect = return_relationships
        response = Response()
        id = 5
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_node_relationships(id, response))

        self.assertEqual(result, RelationshipsOut(relationships=[BasicRelationshipOut(id=5),
                                                                 BasicRelationshipOut(id=6)], links=get_links(router)))
        get_relationships_mock.assert_called_with(id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(NodeService, 'get_relationships')
    def test_get_node_relationships_post_with_error(self, get_relationships_mock):
        get_relationships_mock.return_value = RelationshipsOut( errors={'errors': ['test']})
        response = Response()
        id = 5
        node_router = NodeRouter()

        result = asyncio.run(node_router.get_node_relationships(id, response))

        self.assertEqual(result, RelationshipsOut(errors={'errors': ['test']}, links=get_links(router)))
        get_relationships_mock.assert_called_with(id)
        self.assertEqual(response.status_code, 422)
