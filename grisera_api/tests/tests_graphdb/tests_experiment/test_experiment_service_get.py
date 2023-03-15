import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import BasicActivityExecutionOut
from experiment.experiment_model import *
from models.not_found_model import *

from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from graph_api_service import GraphApiService


class TestExperimentServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_experiment_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Experiment'],
                                      'properties': [{'key': 'experiment_name', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "hasScenario", "id": 0,
             "properties": None}]}
        additional_properties = [PropertyIn(key='test', value="test")]
        experiment = ExperimentOut(experiment_name="test", additional_properties=additional_properties, id=id_node,
                                   activity_executions=[BasicActivityExecutionOut(**{id: 19})])
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.get_experiment(id_node)

        self.assertEqual(result, experiment)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_experiment_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.get_experiment(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_experiment_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.get_experiment(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_experiments(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Experiment'],
                                                  'properties': [{'key': 'experiment_name', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Experiment'],
                                                  'properties': [{'key': 'experiment_name', 'value': 'test2'}]}]}
        experiment_one = BasicExperimentOut(experiment_name="test", id=1, additional_properties=[])
        experiment_two = BasicExperimentOut(experiment_name="test2", id=2, additional_properties=[])
        experiments = ExperimentsOut(experiments=[experiment_one, experiment_two])
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.get_experiments()

        self.assertEqual(result, experiments)
        get_nodes_mock.assert_called_once_with("Experiment")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_experiments_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        experiments = ExperimentsOut(experiments=[])
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.get_experiments()

        self.assertEqual(result, experiments)
        get_nodes_mock.assert_called_once_with("Experiment")
