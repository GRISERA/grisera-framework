from relationship.relationship_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_relationship(*args, **kwargs):
    relationship_out = RelationshipOut(start_node=args[0].start_node, end_node=args[0].end_node, name=args[0].name, id=5, errors=None)
    return relationship_out


class TestRelationshipPost(unittest.TestCase):

    @mock.patch.object(RelationshipService, 'save_relationship')
    def test_relationship_post_without_error(self, mock_service):
        mock_service.side_effect = return_relationship
        response = Response()
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_router = RelationshipRouter()

        result = asyncio.run(relationship_router.create_relationship(relationship, response))

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors=None, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RelationshipService, 'save_relationship')
    def test_relationship_post_with_error(self, mock_service):
        mock_service.return_value = RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors={'errors': ['test']})
        response = Response()
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_router = RelationshipRouter()

        result = asyncio.run(relationship_router.create_relationship(relationship, response))

        self.assertEqual(response.status_code, 422)
