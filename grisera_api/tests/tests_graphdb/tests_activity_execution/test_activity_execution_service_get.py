import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from models.not_found_model import *
from activity_execution.activity_execution_model import *
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from participation.participation_model import BasicParticipationOut
from property.property_model import *

"""TODO: expand unit test for get with depth different from  0"""


class TestActivityExecutionServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_activity_execution_without_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Activity Execution'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        activity_execution = BasicActivityExecutionOut(additional_properties=[], id=id_node)
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.get_activity_execution(id_node)

        self.assertEqual(result, activity_execution)
        get_node_mock.assert_called_once_with(id_node)

    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_get_activity_execution_without_error_with_depth(self, get_node_relationships_mock, get_node_mock):
    #     id_node = 1
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Activity Execution'],
    #                                   'properties': [],
    #                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": id_node, "end_node": 19,
    #          "name": "hasActivity", "id": 0,
    #          "properties": None},
    #         {"start_node": 15, "end_node": id_node,
    #          "name": "hasScenario", "id": 0,
    #          "properties": None},
    #         {"start_node": 16, "end_node": id_node,
    #          "name": "hasScenario", "id": 0,
    #          "properties": None},
    #         {"start_node": 20, "end_node": id_node,
    #          "name": "hasActivityExecution", "id": 0,
    #          "properties": None},
    #     ]}
    #     activity_execution = ActivityExecutionOut(additional_properties=[], id=id_node,
    #                                               activity=BasicActivityOut(**{id: 19}),
    #                                               experiments=[BasicExperimentOut(**{id: 15}),
    #                                                            BasicExperimentOut(**{id: 16})],
    #                                               participations=[BasicParticipationOut(**{id: 20})])
    #     activity_execution_service = ActivityExecutionServiceGraphDB()
    #
    #     result = activity_execution_service.get_activity_execution(id_node)
    #
    #     self.assertEqual(result, activity_execution)
    #     get_node_mock.assert_called_once_with(id_node)
    #     get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_activity_execution_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.get_activity_execution(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_activity_execution_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        activity_execution_service = ActivityExecutionServiceGraphDB()

        result = activity_execution_service.get_activity_execution(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_activity_executions(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Activity Execution'],
                                                  'properties': [{'key': 'test', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Activity Execution'],
                                                  'properties': [{'key': 'test2', 'value': 'test3'}]}]}
        activity_execution_one = BasicActivityExecutionOut(additional_properties=[PropertyIn(key='test', value='test')],
                                                           id=1)
        activity_execution_two = BasicActivityExecutionOut(
            additional_properties=[PropertyIn(key='test2', value='test3')],
            id=2)
        activity_executions = ActivityExecutionsOut(
            activity_executions=[activity_execution_one, activity_execution_two])
        activity_executions_service = ActivityExecutionServiceGraphDB()

        result = activity_executions_service.get_activity_executions()

        self.assertEqual(result, activity_executions)
        get_nodes_mock.assert_called_once_with("Activity Execution")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_activity_executions_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        activity_executions = ActivityExecutionsOut(activity_execution=[])
        activity_executions_service = ActivityExecutionServiceGraphDB()

        result = activity_executions_service.get_activity_executions()

        self.assertEqual(result, activity_executions)
        get_nodes_mock.assert_called_once_with("Activity Execution")
