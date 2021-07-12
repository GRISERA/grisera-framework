import unittest
import unittest.mock as mock

from author.author_model import *
from author.author_service import AuthorService
from graph_api_service import GraphApiService


class TestAuthorService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_author_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'name', 'value': 'test'},
                                                                             {'key': 'institution', 'value': 'testInstitution'}],
                                               "errors": None, 'links': None}
        author = AuthorIn(name='test', institution='testInstitution')
        author_service = AuthorService()

        result = author_service.save_author(author)

        self.assertEqual(result, AuthorOut(name='test', institution='testInstitution',
                                           id=id_node))
        create_node_mock.assert_called_once_with('Author')
        create_properties_mock.assert_called_once_with(id_node, author)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_author_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        author = AuthorIn(name='test', institution='testInstitution')
        author_service = AuthorService()

        result = author_service.save_author(author)

        self.assertEqual(result, AuthorOut(name="test", errors=['error']))
        create_node_mock.assert_called_once_with('Author')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_author_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        author = AuthorIn(name='test', institution='testInstitution')
        author_service = AuthorService()

        result = author_service.save_author(author)

        self.assertEqual(result, AuthorOut(name='test', errors=['error']))
        create_node_mock.assert_called_once_with('Author')
        create_properties_mock.assert_called_once_with(id_node, author)