from node.node_service import NodeService
from node.node_model import *
from database_service import DatabaseService
import unittest
import unittest.mock as mock


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

    @mock.patch.object(DatabaseService, 'get_nodes')
    def test_get_nodes_without_error(self, get_nodes_mock):
        get_nodes_mock.return_value = {'results': [{'data': [{'row': [{}], 'meta': [{'id': '5'}]}]}],
                                      'errors': []}
        label = "Test"
        node_service = NodeService()

        result = node_service.get_nodes(label)

        self.assertEqual(result, NodesOut(nodes=[BasicNodeOut(id=5, labels={"Test"}, properties=[])]))
        get_nodes_mock.assert_called_once_with(label)

    @mock.patch.object(DatabaseService, 'get_nodes')
    def test_get_nodes_with_error(self, get_nodes_mock):
        get_nodes_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}], 'errors': ['error']}
        label = "Test"
        node_service = NodeService()

        result = node_service.get_nodes(label)

        self.assertEqual(result, NodesOut(errors=['error']))
        get_nodes_mock.assert_called_once_with(label)

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
