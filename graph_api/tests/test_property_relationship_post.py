from relationship.relationship_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_relationship(*args, **kwargs):
    node_out = RelationshipOut(start_node=0, end_node=1, name="test", id=args[0], properties=args[1])
    return node_out


class TestRelationshipPropertyPost(unittest.TestCase):

    @mock.patch.object(RelationshipService, 'save_properties')
    def test_properties_for_relationship_post_without_error(self, mock_service):
        mock_service.side_effect = return_relationship
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = RelationshipRouter()

        result = asyncio.run(node_router.create_relationship_properties(id, properties, response))

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test", id=5,
                                                 properties=properties, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RelationshipService, 'save_properties')
    def test_properties_for_relationship_post_with_error(self, mock_service):
        mock_service.return_value = RelationshipOut(errors={'errors': ['test']})
        response = Response()
        id = 5
        properties = [PropertyIn(key="testkey", value="testvalue")]
        node_router = RelationshipRouter()

        result = asyncio.run(node_router.create_relationship_properties(id, properties, response))

        self.assertEqual(response.status_code, 422)
