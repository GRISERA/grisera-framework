import unittest
import unittest.mock as mock
from publication.publication_model import *
from publication.publication_service import PublicationService, AuthorService
from graph_api_service import GraphApiService


def relationship_function(*args, **kwargs):
    if kwargs['name'] == 'hasPublication':
        return {'start_node': 1, 'end_node': 3, 'id': 5, 'name': 'hasPublication', 'errors': ['error']}
    return {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'hasAuthor', 'errors': None}


class TestPublicationService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(AuthorService, 'save_author')
    def test_save_publication_without_errors(self, save_author_mock, create_relationships_mock,
                                             create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node,
                                               'properties': [{'key': 'experiment_name', 'value': 'test'}],
                                               "errors": None, 'links': None}
        author_out = AuthorOut(id=2, name='TestName')
        save_author_mock.return_value = author_out
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2, 'id': 3,
                                                  'name': 'hasAuthor', 'errors': None}
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        authors_out = [author_out, author_out]
        publication = PublicationIn(title='Test', authors=authors)
        publication_service = PublicationService()

        result = publication_service.save_publication(publication)

        self.assertEqual(result, PublicationOut(title='Test', authors=authors_out, id=id_node))
        create_node_mock.assert_called_once_with('Publication')
        create_properties_mock.assert_called_once_with(id_node, publication)
        save_author_mock.assert_called_with(author=authors[0])
        create_relationships_mock.assert_called_with(end_node=2, start_node=1, name="hasAuthor")

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_publication_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        publication = PublicationIn(title='Test', authors=authors)
        publication_service = PublicationService()

        result = publication_service.save_publication(publication)

        self.assertEqual(result, PublicationOut(title='Test', authors=authors, errors=['error']))
        create_node_mock.assert_called_once_with('Publication')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_publication_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        publication = PublicationIn(title='Test', authors=authors)
        publication_service = PublicationService()

        result = publication_service.save_publication(publication)

        self.assertEqual(result, PublicationOut(title='Test', authors=authors, errors=['error']))
        create_node_mock.assert_called_once_with('Publication')
        create_properties_mock.assert_called_once_with(id_node, publication)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(AuthorService, 'save_author')
    def test_save_experiment_with_authors_relationship_error(self, save_author_mock, create_relationships_mock,
                                                             create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'experiment_name', 'value': 'test'}],
                                               "errors": None, 'links': None}
        save_author_mock.return_value = AuthorOut(id=2, name='TestName')
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasAuthor', 'errors': ['error']}
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        publication = PublicationIn(title='Test', authors=authors)
        publication_service = PublicationService()

        result = publication_service.save_publication(publication)

        self.assertEqual(result, PublicationOut(title='Test', authors=authors, errors=['error']))
        create_node_mock.assert_called_once_with('Publication')
        create_properties_mock.assert_called_once_with(id_node, publication)
        save_author_mock.assert_called_once_with(author=authors[0])
        create_relationships_mock.assert_called_once_with(end_node=2, start_node=1, name="hasAuthor")
