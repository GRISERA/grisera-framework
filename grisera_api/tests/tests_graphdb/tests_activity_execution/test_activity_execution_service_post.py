import unittest
import unittest.mock as mock

from activity import BasicActivityOut
from experiment.experiment_model import BasicExperimentOut
from graph_api_service import GraphApiService
from activity_execution.activity_execution_model import *
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from participation.participation_model import BasicParticipationOut

"""TODO: expand unit test for get with depth different from  0"""


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
             "name": "hasActivity", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "hasScenario", "id": 0,
             "properties": None},
            {"start_node": 16, "end_node": id_node,
             "name": "hasScenario", "id": 0,
             "properties": None},
            {"start_node": 20, "end_node": id_node,
             "name": "hasActivityExecution", "id": 0,
             "properties": None},
        ]}
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        activity_execution_in = ActivityExecutionIn(activity_id=2, arrangement_id=3)
        activity_execution_out = ActivityExecutionOut(additional_properties=[], id=id_node,
                                                      activity=BasicActivityOut(**{id: 19}),
                                                      experiments=[BasicExperimentOut(**{id: 15}),
                                                                   BasicExperimentOut(**{id: 16})],
                                                      participations=[BasicParticipationOut(**{id: 20})])
        calls = [mock.call(2), mock.call(3), mock.call(1)]
        activity_execution_service = ActivityExecutionServiceGraphDB()

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
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.save_activity_execution(activity_execution)

        self.assertEqual(result, ActivityExecutionOut(errors=['error']))
        create_node_mock.assert_called_once_with('`Activity Execution`')
