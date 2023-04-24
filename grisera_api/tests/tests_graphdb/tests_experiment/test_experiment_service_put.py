import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import BasicActivityExecutionOut
from experiment.experiment_model import *
from models.not_found_model import *

from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from graph_api_service import GraphApiService


class TestExperimentServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    def test_update_experiment_without_error(self, delete_node_properties_mock,
                                             get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Experiment'],
                                      'properties': [{'key': 'experiment_name', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment_in = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
        experiment_out = BasicExperimentOut(experiment_name="test", additional_properties=additional_properties, id=id_node)
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.update_experiment(id_node, experiment_in)

        self.assertEqual(result, experiment_out)
        get_node_mock.assert_called_once_with(id_node)
        create_properties_mock.assert_called_once_with(id_node, experiment_in)

    # @mock.patch.object(GraphApiService, 'create_properties')
    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'delete_node_properties')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_update_experiment_without_error(self, get_node_relationships_mock, delete_node_properties_mock,
    #                                          get_node_mock, create_properties_mock):
    #     id_node = 1
    #     create_properties_mock.return_value = {}
    #     delete_node_properties_mock.return_value = {}
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Experiment'],
    #                                   'properties': [{'key': 'experiment_name', 'value': 'test'},
    #                                                  {'key': 'test', 'value': 'test'}],
    #                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": id_node, "end_node": 19,
    #          "name": "hasScenario", "id": 0,
    #          "properties": None}]}
    #     additional_properties = [PropertyIn(key='test', value='test')]
    #     experiment_in = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
    #     experiment_out = ExperimentOut(experiment_name="test", additional_properties=additional_properties, id=id_node,
    #                                    activity_executions=[BasicActivityExecutionOut(**{id: 19})])
    #     experiment_service = ExperimentServiceGraphDB()
    #
    #     result = experiment_service.update_experiment(id_node, experiment_in)
    #
    #     self.assertEqual(result, experiment_out)
    #     get_node_mock.assert_called_once_with(id_node)
    #     create_properties_mock.assert_called_once_with(id_node, experiment_in)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_experiment_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        experiment_in = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.update_experiment(id_node, experiment_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_experiment_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        experiment_in = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.update_experiment(id_node, experiment_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
