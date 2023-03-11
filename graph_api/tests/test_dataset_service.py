import unittest
import unittest.mock as mock

from database_service import DatabaseService
from relationship.relationship_model import *
from relationship.relationship_service import RelationshipService


class TestRelationshipService(unittest.TestCase):

    def setUp(self):
        self.database_name = "neo4j"

    @mock.patch.object(DatabaseService, 'create_relationship')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_relationship_without_error(self, node_exists_mock, create_relationship_mock):
        create_relationship_mock.return_value = {'results': [{'data': [{'meta': [{'id': '5'}]}]}],
                                                 'errors': []}
        node_exists_mock.return_value = True
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship, self.database_name)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors=None))
        create_relationship_mock.assert_called_once_with(relationship, self.database_name)

    @mock.patch.object(DatabaseService, 'create_relationship')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_relationship_with_error(self, node_exists_mock, create_relationship_mock):
        create_relationship_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                                 'errors': ['error']}
        node_exists_mock.return_value = True
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship, self.database_name)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", errors=['error']))
        create_relationship_mock.assert_called_once_with(relationship, self.database_name)

    @mock.patch.object(DatabaseService, 'create_relationship')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_relationship_without_nodes(self, node_exists_mock, create_relationship_mock):
        create_relationship_mock.return_value = {'results': [{'data': [{'meta': [{'id': '5'}]}]}],
                                                 'errors': []}
        node_exists_mock.return_value = False
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship, self.database_name)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test",
                                                 errors={"errors": "not matching node id"}))
        create_relationship_mock.assert_not_called()

    @mock.patch.object(DatabaseService, 'get_relationship')
    def test_get_relationship_without_error(self, get_relationship_mock):
        get_relationship_mock.return_value = {
            'results': [{'data': [{'row': [0, 1, "test", 5]}]}], 'errors': []}
        relationship_service = RelationshipService()

        result = relationship_service.get_relationship(5, self.database_name)

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test", id=5))
        get_relationship_mock.assert_called_once_with(5, self.database_name)

    @mock.patch.object(DatabaseService, 'get_relationship')
    def test_get_relationship_without_relationships_exists(self, get_relationship_mock):
        get_relationship_mock.return_value = {'results': [{'data': []}],
                                               'errors': ['error']}
        relationship_service = RelationshipService()

        result = relationship_service.get_relationship(5, self.database_name)

        self.assertEqual(result, RelationshipOut(errors="Relationship not found"))
        get_relationship_mock.assert_called_once_with(5, self.database_name)

    @mock.patch.object(RelationshipService, 'get_relationship')
    @mock.patch.object(DatabaseService, 'delete_relationship')
    def test_delete_relationship_without_error(self, delete_relationship_mock, get_relationship_mock):
        delete_relationship_mock.return_value = {'results': [{'data': [{'meta': [{'id': '5'}]}]}],
                                                 'errors': []}
        get_relationship_mock.return_value = RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors=None)
        relationship_id = 5
        relationship_service = RelationshipService()

        result = relationship_service.delete_relationship(relationship_id, self.database_name)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors=None))
        delete_relationship_mock.assert_called_once_with(relationship_id, self.database_name)
        get_relationship_mock.assert_called_once_with(relationship_id, self.database_name)

    @mock.patch.object(RelationshipService, 'get_relationship')
    @mock.patch.object(DatabaseService, 'delete_relationship')
    def test_delete_relationship_with_error(self, delete_relationship_mock, get_relationship_mock):
        delete_relationship_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                                 'errors': ['error']}
        get_relationship_mock.return_value = None
        relationship_id = 5
        relationship_service = RelationshipService()

        result = relationship_service.delete_relationship(relationship_id, self.database_name)

        self.assertEqual(result, RelationshipOut(errors=['error']))
        delete_relationship_mock.assert_called_once_with(relationship_id, self.database_name)
        get_relationship_mock.assert_called_once_with(relationship_id, self.database_name)

    @mock.patch.object(DatabaseService, 'create_relationship_properties')
    @mock.patch.object(DatabaseService, 'relationship_exist')
    def test_save_properties_without_error(self, relationship_exist_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': [0, "test", 1, {"testkey": "testvalue"}]}]}],
                                               'errors': []}
        relationship_exist_mock.return_value = True
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties, database_name=self.database_name)

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test",
                                                 id=5, properties=properties))
        create_properties_mock.assert_called_once_with(5, properties, self.database_name)

    @mock.patch.object(DatabaseService, 'create_relationship_properties')
    @mock.patch.object(DatabaseService, 'relationship_exist')
    def test_save_properties_with_error(self, relationship_exist_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': []}]}],
                                               'errors': ['error']}
        relationship_exist_mock.return_value = True
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties, database_name=self.database_name)

        self.assertEqual(result, RelationshipOut(errors=['error']))
        create_properties_mock.assert_called_once_with(5, properties, self.database_name)

    @mock.patch.object(DatabaseService, 'create_relationship_properties')
    @mock.patch.object(DatabaseService, 'relationship_exist')
    def test_save_properties_without_nodes(self, relationship_exist_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': [0, "test", 1, {"testkey": "testvalue"}]}]}],
                                               'errors': []}
        relationship_exist_mock.return_value = False
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties, database_name=self.database_name)

        self.assertEqual(result, RelationshipOut(id=5, errors={"errors": "not matching id"}))
