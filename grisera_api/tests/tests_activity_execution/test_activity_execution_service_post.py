import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from activity_execution.activity_execution_model import *
from activity_execution.activity_execution_service import ActivityExecutionService


class TestActivityExecutionServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_activity_execution_without_errors(self, get_node_relationships_mock, get_node_mock,
                                                    create_relationships_mock, create_properties_mock,
                                                    create_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Activity Execution'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        additional_properties = []
        activity_execution_in = ActivityExecutionIn(activity_id=2, arrangement_id=3)
        activity_execution_out = ActivityExecutionOut(additional_properties=additional_properties, relations=
                                                      [RelationInformation(second_node_id=19, name="testRelation",
                                                                           relation_id=0)],
                                                      reversed_relations=
                                                      [RelationInformation(second_node_id=15,
                                                                           name="testReversedRelation",
                                                                           relation_id=0)], id=id_node)
        calls = [mock.call(2), mock.call(3), mock.call(1)]
        activity_execution_service = ActivityExecutionService()

        result = activity_execution_service.save_activity_execution(activity_execution_in)

        self.assertEqual(result, activity_execution_out)
        create_node_mock.assert_called_once_with('`Activity Execution`')
        # create_properties_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_activity_execution_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        activity_execution = ActivityExecutionIn(activity_id=2, arrangement_id=3)
        activity_execution_service = ActivityExecutionService()

        result = activity_execution_service.save_activity_execution(activity_execution)

        self.assertEqual(result, ActivityExecutionOut(errors=['error']))
        create_node_mock.assert_called_once_with('`Activity Execution`')
