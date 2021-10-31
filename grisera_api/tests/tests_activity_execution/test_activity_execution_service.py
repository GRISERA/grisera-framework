import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import *
from activity_execution.activity_execution_service import ActivityExecutionService
from graph_api_service import GraphApiService

from activity.activity_service import ActivityService
from activity.activity_model import ActivitiesOut, BasicActivityOut
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_model import ArrangementsOut, BasicArrangementOut


class TestActivityExecutionService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ActivityService, 'get_activities')
    @mock.patch.object(ArrangementService, 'get_arrangements')
    def test_save_activity_execution_without_error(self, get_arrangements_mock, get_activities_mock, create_relationships_mock,
                                                   create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'activity',
                                                                              'value': 'group'},
                                                                             {'key': 'arrangement_type',
                                                                              'value': 'personal group'}
                                                                             ], "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]

        create_relationships_mock.return_value = {'id': 3, 'start_node': 1, "errors": None, 'links': None}
        get_activities_mock.return_value = ActivitiesOut(activities=[BasicActivityOut(id=4, activity='group')])

        create_relationships_mock.return_value = {'id': 5, 'start_node': 1, "errors": None, 'links': None}
        get_arrangements_mock.return_value = \
            ArrangementsOut(arrangements=[BasicArrangementOut(id=6, arrangement_type='personal group')])

        calls = [mock.call(start_node=id_node, end_node=4, name="hasActivity"),
                 mock.call(start_node=id_node, end_node=6, name="hasArrangement")]

        activity_execution = ActivityExecutionIn(activity='group', arrangement_type='personal group',
                                                 additional_properties=additional_properties)
        activity_execution_service = ActivityExecutionService()

        result = activity_execution_service.save_activity_execution(activity_execution)

        self.assertEqual(result, ActivityExecutionOut(activity='group', arrangement_type='personal group', id=id_node,
                                                      additional_properties=additional_properties))

        create_node_mock.assert_called_once_with('ActivityExecution')
        create_properties_mock.assert_called_once_with(id_node, activity_execution)
        get_activities_mock.assert_called_once()
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_activity_execution_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        activity_execution = ActivityExecutionIn(activity='group', arrangement_type='personal group')
        activity_execution_service = ActivityExecutionService()

        result = activity_execution_service.save_activity_execution(activity_execution)

        self.assertEqual(result, ActivityExecutionOut(activity='group', arrangement_type='personal group'
                                                      , errors=['error']))
        create_node_mock.assert_called_once_with('ActivityExecution')

    # @mock.patch.object(GraphApiService, 'create_node')
    # @mock.patch.object(GraphApiService, 'create_properties')
    # def test_save_activity_execution_with_properties_error(self, create_properties_mock, create_node_mock):
    #     id_node = 1
    #     create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
    #     create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
    #     activity_execution = ActivityExecutionIn(activity='group', arrangement_type='personal group')
    #     activity_execution_service = ActivityExecutionService()
    #
    #     result = activity_execution_service.save_activity_execution(activity_execution)
    #
    #     self.assertEqual(result, ActivityExecutionOut(activity='group', arrangement_type='personal group',
    #                                                   errors=['error']))
    #     create_node_mock.assert_called_once_with('ActivityExecution')
    #     create_properties_mock.assert_called_once_with(id_node, activity_execution)
