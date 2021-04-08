from relationship.relationship_service import RelationshipService
from relationship.relationship_model import *
import unittest
import unittest.mock as mock
from requests import Response
import json


class TestRelationshipPostService(unittest.TestCase):

    @mock.patch('relationship.relationship_service.requests')
    def test_relationship_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [
                                        {'data': [
                                            {'meta': [
                                                {'id': '5'}]
                                            }]
                                        }],
                                        'errors': []}).encode('utf-8')
        mock_requests.post.return_value = response
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", id=5, errors=None))

    @mock.patch('relationship.relationship_service.requests')
    def test_relationship_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [{'data': [{'meta': [{}]}]}],
                                        'errors': ['error']}).encode('utf-8')
        mock_requests.post.return_value = response
        relationship = RelationshipIn(start_node=1, end_node=2, name="test")
        relationship_service = RelationshipService()

        result = relationship_service.save_relationship(relationship)

        self.assertEqual(result, RelationshipOut(start_node=1, end_node=2, name="test", errors=['error']))
