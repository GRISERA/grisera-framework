import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import *
from models.not_found_model import *

from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from graph_api_service import GraphApiService


class TestActivityExecutionServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_activity_execution_without_error(self, get_node_relationships_mock, delete_node_properties_mock,
                                                     get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Activity Execution'],
                                      'properties': [{'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        activity_execution_in = ActivityExecutionPropertyIn(id=id_node, additional_properties=additional_properties)
        activity_execution_out = ActivityExecutionOut(additional_properties= additional_properties, id=id_node,
                                                      relations=[RelationInformation(second_node_id=19,
                                                                                     name="testRelation",
                                                                                     relation_id=0)],
                                                      reversed_relations=[RelationInformation(second_node_id=15,
                                                                                             name="testReversedRelation",
                                                                                             relation_id=0)])
        calls = [mock.call(1)]
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.update_activity_execution(id_node, activity_execution_in)

        self.assertEqual(result, activity_execution_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_called_once_with(id_node, activity_execution_in)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_activity_execution_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        additional_properties = [PropertyIn(key='identifier', value=5)]
        activity_execution_in = ActivityExecutionPropertyIn(id=id_node,
                                                            additional_properties=additional_properties)
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.update_activity_execution(id_node, activity_execution_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_activity_execution_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        additional_properties = [PropertyIn(key='identifier', value=5)]
        activity_execution_in = ActivityExecutionPropertyIn(id=id_node,
                                                            additional_properties=additional_properties)
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.update_activity_execution(id_node, activity_execution_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
