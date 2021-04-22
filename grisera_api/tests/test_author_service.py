import json
import unittest
import unittest.mock as mock
from author.author_model import *
from author.author_service import AuthorService
from requests import Response


class TestAuthorPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_author_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        author = AuthorIn(name="test")
        author_service = AuthorService()

        result = author_service.save_author(author)

        self.assertEqual(result, AuthorOut(id=1, name="test"))

    @mock.patch('graph_api_service.requests')
    def test_author_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': {'name':'test'}, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        author = AuthorIn(name="test")
        author_service = AuthorService()

        result = author_service.save_author(author)

        self.assertEqual(result, AuthorOut(name="test", errors={'error': 'test'}))
