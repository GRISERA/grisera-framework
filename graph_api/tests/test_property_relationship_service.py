from relationship.relationship_service import RelationshipService
from relationship.relationship_model import *
import unittest
import unittest.mock as mock
from requests import Response
import json


class TestPropertyRelationshipPostService(unittest.TestCase):

    @mock.patch('database_service.requests')
    def test_property_relationship_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [
                                        {'data': [
                                            {'row': [0, "test", 1, {"testkey": "testvalue"}]
                                            }]
                                        }],
                                        'errors': []}).encode('utf-8')
        mock_requests.post.return_value = response
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, RelationshipOut(start_node=0, end_node=1, name="test",
                                                 id=5, properties=properties))

    @mock.patch('database_service.requests')
    def test_property_relationship_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'results': [{'data': [{'row': []}]}],
                                        'errors': ['error']}).encode('utf-8')
        mock_requests.post.return_value = response
        relationship_service = RelationshipService()
        properties = [PropertyIn(key="testkey", value="testvalue")]

        result = relationship_service.save_properties(id=5, properties=properties)

        self.assertEqual(result, RelationshipOut(errors=['error']))
