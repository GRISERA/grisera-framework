import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import *
from models.not_found_model import *

from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from graph_api_service import GraphApiService


class TestActivityExecutionServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_activity_execution_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Activity Execution'],
                                                                      'properties': [],
                                                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        activity_execution = ActivityExecutionOut(additional_properties=[], id=id_node,
                                                  relations=[RelationInformation(second_node_id=19,
                                                                                 name="testRelation",
                                                                                 relation_id=0)],
                                                  reversed_relations=[RelationInformation(second_node_id=15,
                                                                                          name="testReversedRelation",
                                                                                          relation_id=0)])
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.delete_activity_execution(id_node, dataset_name)

        self.assertEqual(result, activity_execution)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
        delete_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_activity_execution_without_participant_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.delete_activity_execution(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_activity_execution_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.delete_activity_execution(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)