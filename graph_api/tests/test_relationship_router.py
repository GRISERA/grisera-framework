import asyncio
import unittest
import unittest.mock as mock

from relationship.relationship_router import *


def return_relationship(*args, **kwargs):
    return RelationshipOut(start_node=args[0].start_node, end_node=args[0].end_node,
                                       name=args[0].name, id=5, errors=None)


def return_relationship_with_properties(*args, **kwargs):
    return RelationshipOut(start_node=0, end_node=1, name="test", id=args[0], properties=args[1])


class TestRelationshipRouter(unittest.TestCase):

    @mock.patch.object(RelationshipService, 'save_relationship')
    def test_create_relationship_without_error(self, save_relationship_mock):
        save_relationship_mock.side_effect = return_relationship
        response = Response()
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_router = RelationshipRouter()

        result = asyncio.run(relationship_router.create_relationship(relationship, response))

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5,
                                                 errors=None, links=get_links(router)))
        save_relationship_mock.assert_called_with(relationship)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RelationshipService, 'save_relationship')
    def test_create_relationship_with_error(self, save_relationship_mock):
        save_relationship_mock.return_value = RelationshipOut(start_node=1, end_node=2, name="test",
                                                    id=5, errors={'errors': ['test']})
        response = Response()
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_router = RelationshipRouter()

        result = asyncio.run(relationship_router.create_relationship(relationship, response))

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5,
                                                 errors={'errors': ['test']}, links=get_links(router)))
        save_relationship_mock.assert_called_with(relationship)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(RelationshipService, 'save_properties')
    def test_create_relationship_properties_without_error(self, save_properties_mock):
        save_properties_mock.side_effect = return_relationship_with_properties
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = RelationshipRouter()

        result = asyncio.run(node_router.create_relationship_properties(id, properties, response))

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test", id=5,
                                                 properties=properties, links=get_links(router)))
        save_properties_mock.assert_called_once_with(id, properties)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RelationshipService, 'save_properties')
    def test_create_relationship_properties_with_error(self, save_properties_mock):
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        save_properties_mock.return_value = RelationshipOut(start_node=0, end_node=1, name="test", properties=properties,
                                                    id=5, errors={'errors': ['test']})
        node_router = RelationshipRouter()

        result = asyncio.run(node_router.create_relationship_properties(id, properties, response))

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test", properties=properties,
                                                 id=5, errors={'errors': ['test']}, links=get_links(router)))
        save_properties_mock.assert_called_once_with(id, properties)
        self.assertEqual(response.status_code, 422)
