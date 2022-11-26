import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from experiment.experiment_model import *
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB


class TestExperimentServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_experiment_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'experiment_name', 'value': 'test'},
                                                                             {'key': 'test', 'value': 'test'}],
                                               "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", additional_properties=additional_properties,
                                               id=id_node))
        create_node_mock.assert_called_once_with('Experiment')
        create_properties_mock.assert_called_once_with(id_node, experiment)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_experiment_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", additional_properties=additional_properties,
                                               errors=['error']))
        create_node_mock.assert_called_once_with('Experiment')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_experiment_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", additional_properties=additional_properties,
                                               errors=['error']))
        create_node_mock.assert_called_once_with('Experiment')
        create_properties_mock.assert_called_once_with(id_node, experiment)
