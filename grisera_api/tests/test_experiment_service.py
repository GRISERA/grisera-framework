import json
import unittest
import unittest.mock as mock
from experiment.experiment_model import *
from experiment.experiment_service import ExperimentService, AuthorService, PublicationService
from graph_api_service import GraphApiService


def relationship_function(*args, **kwargs):
    if kwargs['name'] == 'hasPublication':
        return {'start_node': 1, 'end_node': 3, 'id': 5, 'name': 'hasPublication', 'errors': ['error']}
    return {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'hasAuthor', 'errors': None}


class TestExperimentService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(AuthorService, 'save_author')
    @mock.patch.object(PublicationService, 'save_publication')
    def test_save_experiment_without_errors(self, save_publication_mock, save_author_mock, create_relationships_mock,
                                            create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'experiment_name', 'value': 'test'}],
                                               "errors": None, 'links': None}
        save_author_mock.return_value = AuthorOut(id=2, name='TestName')
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        save_publication_mock.return_value = PublicationOut(id=3, authors=authors, title='Test')
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'has', 'errors': None}
        publication = PublicationIn(title='Test', authors=authors)
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]
        experiment = ExperimentIn(experiment_name="test", authors=authors, publication=publication,
                                  additional_properties=additional_properties)
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", id=id_node,
                                               authors=[AuthorOut(id=2, name='TestName'), AuthorOut(id=2, name='TestName')],
                                               publication=PublicationOut(id=3, authors=authors, title='Test'),
                                               additional_properties=additional_properties))
        create_node_mock.assert_called_once_with('Experiment')
        create_properties_mock.assert_called_once_with(id_node, experiment)
        save_author_mock.assert_called_with(author=authors[0])
        save_author_mock.assert_called_with(author=authors[1])
        save_publication_mock.assert_called_once_with(publication=publication)
        create_relationships_mock.assert_called_with(end_node=3, start_node=1, name="hasPublication")

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_experiment_with_experiment_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        experiment = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", errors=['error']))
        create_node_mock.assert_called_once_with('Experiment')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_experiment_with_experiment_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        experiment = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", errors=['error']))
        create_node_mock.assert_called_once_with('Experiment')
        create_properties_mock.assert_called_once_with(id_node, experiment)

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
        experiment = ExperimentIn(experiment_name="test", authors=authors)
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", authors=authors, errors=['error']))
        create_node_mock.assert_called_once_with('Experiment')
        create_properties_mock.assert_called_once_with(id_node, experiment)
        save_author_mock.assert_called_once_with(author=authors[0])
        create_relationships_mock.assert_called_once_with(end_node=2, start_node=1, name="hasAuthor")

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(AuthorService, 'save_author')
    @mock.patch.object(PublicationService, 'save_publication')
    def test_save_experiment_with_publication_relationship_error(self, save_publication_mock, save_author_mock,
                                                                 create_relationships_mock, create_properties_mock,
                                                                 create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'experiment_name', 'value': 'test'}],
                                               "errors": None, 'links': None}
        save_author_mock.return_value = AuthorOut(id=2, name='TestName')
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        save_publication_mock.return_value = PublicationOut(id=3, authors=authors, title='Test')
        create_relationships_mock.side_effect = relationship_function
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        publication = PublicationIn(title='Test', authors=authors)
        experiment = ExperimentIn(experiment_name="test", authors=authors, publication=publication)
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", publication=publication, errors=['error']))
        create_node_mock.assert_called_once_with('Experiment')
        create_properties_mock.assert_called_once_with(id_node, experiment)
        save_author_mock.assert_called_with(author=authors[0])
        save_author_mock.assert_called_with(author=authors[1])
        create_relationships_mock.assert_called_with(end_node=3, start_node=1, name="hasPublication")
        save_publication_mock.assert_called_once_with(publication=publication)
