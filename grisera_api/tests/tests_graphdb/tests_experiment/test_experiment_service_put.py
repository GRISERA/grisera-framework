import unittest
import unittest.mock as mock

from experiment.experiment_model import *
from models.not_found_model import *

from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from graph_api_service import GraphApiService


class TestExperimentServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_experiment_without_error(self, get_node_relationships_mock, delete_node_properties_mock,
                                             get_node_mock, create_properties_mock):
        database_name = "neo4j"
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Experiment'],
                                      'properties': [{'key': 'experiment_name', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment_in = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
        experiment_out = ExperimentOut(experiment_name="test", additional_properties=additional_properties, id=id_node,
                                       relations=
                                       [RelationInformation(second_node_id=19, name="testRelation", relation_id=0)],
                                       reversed_relations=
                                       [RelationInformation(second_node_id=15, name="testReversedRelation",
                                                            relation_id=0)])
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.update_experiment(id_node, experiment_in, database_name)

        self.assertEqual(result, experiment_out)
        get_node_mock.assert_called_once_with(id_node, database_name)
        create_properties_mock.assert_called_once_with(id_node, experiment_in, database_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_experiment_without_participant_label(self, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        experiment_in = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.update_experiment(id_node, experiment_in, database_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, database_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_experiment_with_error(self, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        experiment_in = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentServiceGraphDB()

        result = experiment_service.update_experiment(id_node, experiment_in, database_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, database_name)
