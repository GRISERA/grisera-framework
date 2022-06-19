import unittest
import unittest.mock as mock

from database_service import DatabaseService
from node.node_model import *
from node.node_service import NodeService
from relationship.relationship_model import *


class NodeServiceTestCase(unittest.TestCase):

    @mock.patch.object(DatabaseService, 'create_node')
    def test_save_node_without_error(self, create_node_mock):
        create_node_mock.return_value = {'results': [{'data': [{'meta': [{'id': '5'}]}]}],
                                      'errors': []}
        node = NodeIn(labels={"test"})
        node_service = NodeService()

        result = node_service.save_node(node)

        self.assertEqual(result, NodeOut(id=5, labels={"test"}))
        create_node_mock.assert_called_once_with(node)

    @mock.patch.object(DatabaseService, 'create_node')
    def test_save_node_with_error(self, create_node_mock):
        create_node_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                      'errors': ['error']}
        node = NodeIn(labels={"test"})
        node_service = NodeService()

        result = node_service.save_node(node)

        self.assertEqual(result, NodeOut(errors=['error']))
        create_node_mock.assert_called_once_with(node)

    @mock.patch.object(DatabaseService, 'get_node')
    def test_get_node_with_existing_node(self, get_node_mock):
        get_node_mock.return_value = {'results': [{'data': [{'row': [{'key': 'value'}, ["Test"]]}]}], 'errors': []}
        node_id = 1
        node_service = NodeService()

        result = node_service.get_node(node_id)

        self.assertEqual(result, NodeOut(id=1, properties=[PropertyIn(key='key', value='value')], labels={"Test"}))
        get_node_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'get_node')
    def test_get_node_without_existing_node(self, get_node_mock):
        get_node_mock.return_value = {'results': [{'data': []}], 'errors': []}
        node_id = 1
        node_service = NodeService()

        result = node_service.get_node(node_id)

        self.assertEqual(result, NodeOut(errors='Node not found'))
        get_node_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'get_nodes')
    def test_get_nodes_without_error(self, get_nodes_mock):
        get_nodes_mock.return_value = {'results': [{'data': [{'row': [{}], 'meta': [{'id': '5'}]}]}],
                                       'errors': []}
        label = "Test"
        properties_keys = list[str]
        properties_values = list[str]
        node_service = NodeService()

        result = node_service.get_nodes(label, properties_keys, properties_values)

        self.assertEqual(result, NodesOut(nodes=[BasicNodeOut(id=5, labels={"Test"}, properties=[])]))
        get_nodes_mock.assert_called_once_with(label, properties_keys, properties_values)

    @mock.patch.object(DatabaseService, 'get_nodes')
    def test_get_nodes_with_error(self, get_nodes_mock):
        get_nodes_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}], 'errors': ['error']}
        label = "Test"
        properties_keys = list[str]
        properties_values = list[str]
        node_service = NodeService()

        result = node_service.get_nodes(label, properties_keys, properties_values)

        self.assertEqual(result, NodesOut(errors=['error']))
        get_nodes_mock.assert_called_once_with(label, properties_keys, properties_values)

    @mock.patch.object(NodeService, 'get_node')
    @mock.patch.object(DatabaseService, 'delete_node')
    def test_delete_node_without_error(self, delete_node_mock, get_node_mock):
        delete_node_mock.return_value = {'results': [{'data': [{'row': [{'key': 'value'}, ["Test"]]}]}], 'errors': []}
        get_node_mock.return_value = NodeOut(id=1, properties=[PropertyIn(key='key', value='value')], labels={"Test"})
        node_id = 1
        node_service = NodeService()

        result = node_service.delete_node(node_id)

        self.assertEqual(result, NodeOut(id=1, properties=[PropertyIn(key='key', value='value')], labels={"Test"}))
        delete_node_mock.assert_called_once_with(node_id)
        get_node_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'get_node')
    @mock.patch.object(DatabaseService, 'delete_node')
    def test_delete_node_with_error(self, delete_node_mock, get_node_mock):
        delete_node_mock.return_value = {'results': [{'data': []}], 'errors': ['error']}
        node_id = 1
        node_service = NodeService()

        result = node_service.delete_node(node_id)

        self.assertEqual(result, NodeOut(errors=['error']))
        delete_node_mock.assert_called_once_with(node_id)
        get_node_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'get_relationships')
    def test_get_relationships_without_error(self, get_relationships_mock):
        get_relationships_mock.return_value = {'results': [{'data': [{'row': ['1', '2', 'Test', '0']}]}], 'errors': []}
        node_id = 1
        node_service = NodeService()

        result = node_service.get_relationships(node_id)

        self.assertEqual(result, RelationshipsOut(relationships=[BasicRelationshipOut(start_node=1, end_node=2,
                                                  id=0, name="Test")]))
        get_relationships_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'get_relationships')
    def test_get_relationships_with_error(self, get_relationships_mock):
        get_relationships_mock.return_value = {'results': [{'data': []}], 'errors': ['error']}
        node_id = 1
        node_service = NodeService()

        result = node_service.get_relationships(node_id)

        self.assertEqual(result, RelationshipsOut(errors=["error"]))
        get_relationships_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'create_node_properties')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_properties_without_error(self, node_exists_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': [['test'], {'testkey': 'testvalue'}],
                                                                      'meta': [{}]}]}],
                                               'errors': []}
        node_exists_mock.return_value = True
        node_service = NodeService()
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_id = 5

        result = node_service.save_properties(id=node_id, properties=properties)

        self.assertEqual(result, NodeOut(labels={"test"}, id=node_id, properties=properties))
        create_properties_mock.assert_called_once_with(node_id, properties)

    @mock.patch.object(DatabaseService, 'create_node_properties')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_properties_with_error(self, node_exists_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                               'errors': ['error']}
        node_exists_mock.return_value = True
        node_service = NodeService()
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_id = 5

        result = node_service.save_properties(id=node_id, properties=properties)

        self.assertEqual(result, NodeOut(errors=['error']))

    @mock.patch.object(DatabaseService, 'create_node_properties')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_properties_without_node(self, node_exists_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                               'errors': []}
        node_exists_mock.return_value = False
        node_service = NodeService()
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_id = 5

        result = node_service.save_properties(id=node_id, properties=properties)

        self.assertEqual(result, NodeOut(id=node_id, errors={"errors": "not matching id"}))

    @mock.patch.object(NodeService, 'get_node')
    @mock.patch.object(DatabaseService, 'delete_node_properties')
    def test_delete_node_properties_without_error(self, delete_node_properties_mock, get_node_mock):
        delete_node_properties_mock.return_value = {'results': [{'data': [{'row': [{'key': 'value'}, ["Test"]]}]}],
                                                    'errors': []}
        get_node_mock.return_value = NodeOut(id=1, properties=[PropertyIn(key='key', value='value')], labels={"Test"})
        node_id = 1
        node_service = NodeService()

        result = node_service.delete_node_properties(node_id)

        self.assertEqual(result, NodeOut(id=1, properties=[PropertyIn(key='key', value='value')], labels={"Test"}))
        delete_node_properties_mock.assert_called_once_with(node_id)
        get_node_mock.assert_called_once_with(node_id)

    @mock.patch.object(DatabaseService, 'get_node')
    @mock.patch.object(DatabaseService, 'delete_node_properties')
    def test_delete_node_properties_with_error(self, delete_node_properties_mock, get_node_mock):
        delete_node_properties_mock.return_value = {'results': [{'data': []}], 'errors': ['error']}
        node_id = 1
        node_service = NodeService()

        result = node_service.delete_node_properties(node_id)

        self.assertEqual(result, NodeOut(errors=['error']))
        delete_node_properties_mock.assert_called_once_with(node_id)
        get_node_mock.assert_called_once_with(node_id)
