import unittest
import unittest.mock as mock

from activity import BasicActivityOut
from activity_execution.activity_execution_model import *
from experiment.experiment_model import BasicExperimentOut
from models.not_found_model import *

from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from graph_api_service import GraphApiService
from participation.participation_model import BasicParticipationOut

"""TODO: expand unit test for get with depth different from  0"""


class TestActivityExecutionServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_activity_execution_without_error(self, get_node_relationships_mock, get_node_mock,
                                                     delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Activity Execution'],
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
        activity_execution = ActivityExecutionOut(additional_properties=[], id=id_node,
                                                  activity=BasicActivityOut(**{id: 19}),
                                                  experiments=[BasicExperimentOut(**{id: 15}),
                                                               BasicExperimentOut(**{id: 16})],
                                                  participations=[BasicParticipationOut(**{id: 20})])
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.delete_activity_execution(id_node)

        self.assertEqual(result, activity_execution)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_activity_execution_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.delete_activity_execution(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_activity_execution_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.delete_activity_execution(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
