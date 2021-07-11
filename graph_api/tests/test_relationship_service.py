from relationship.relationship_service import RelationshipService
from relationship.relationship_model import *
from database_service import DatabaseService
import unittest
import unittest.mock as mock


class TestRelationshipService(unittest.TestCase):

    @mock.patch.object(DatabaseService, 'create_relationship')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_relationship_without_error(self, node_exists_mock, create_relationship_mock):
        create_relationship_mock.return_value = {'results': [{'data': [{'meta': [{'id': '5'}]}]}],
                                                 'errors': []}
        node_exists_mock.return_value = True
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors=None))
        create_relationship_mock.assert_called_once_with(relationship)

    @mock.patch.object(DatabaseService, 'create_relationship')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_relationship_with_error(self, node_exists_mock, create_relationship_mock):
        create_relationship_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}],
                                                 'errors': ['error']}
        node_exists_mock.return_value = True
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", errors=['error']))
        create_relationship_mock.assert_called_once_with(relationship)

    @mock.patch.object(DatabaseService, 'create_relationship')
    @mock.patch.object(DatabaseService, 'node_exists')
    def test_save_relationship_without_nodes(self, node_exists_mock, create_relationship_mock):
        create_relationship_mock.return_value = {'results': [{'data': [{'meta': [{'id': '5'}]}]}],
                                                 'errors': []}
        node_exists_mock.return_value = False
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test",
                                                 errors={"errors": "not matching node id"}))
        create_relationship_mock.assert_not_called()

    @mock.patch.object(DatabaseService, 'create_relationship_properties')
    @mock.patch.object(DatabaseService, 'relationship_exist')
    def test_save_properties_without_error(self, relationship_exist_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': [0, "test", 1, {"testkey": "testvalue"}]}]}],
                                               'errors': []}
        relationship_exist_mock.return_value = True
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test",
                                                 id=5, properties=properties))
        create_properties_mock.assert_called_once_with(5, properties)

    @mock.patch.object(DatabaseService, 'create_relationship_properties')
    @mock.patch.object(DatabaseService, 'relationship_exist')
    def test_save_properties_with_error(self, relationship_exist_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': []}]}],
                                               'errors': ['error']}
        relationship_exist_mock.return_value = True
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, RelationshipOut(errors=['error']))
        create_properties_mock.assert_called_once_with(5, properties)

    @mock.patch.object(DatabaseService, 'create_relationship_properties')
    @mock.patch.object(DatabaseService, 'relationship_exist')
    def test_save_properties_without_nodes(self, relationship_exist_mock, create_properties_mock):
        create_properties_mock.return_value = {'results': [{'data': [{'row': [0, "test", 1, {"testkey": "testvalue"}]}]}],
                                               'errors': []}
        relationship_exist_mock.return_value = False
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, RelationshipOut(id=5, errors={"errors": "not matching id"}))
