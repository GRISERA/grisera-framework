import unittest
import unittest.mock as mock
from activity.activity_model import *
from activity.activity_service import ActivityService
from graph_api_service import GraphApiService


class TestActivityService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_activity_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'identifier', 'value': 2},
                                                                             {'key': 'name', 'value': 'test'},
                                                                             {'key': 'type', 'value': 'group'}],
                                               "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]
        activity = ActivityIn(identifier=2, name='test', type='group', additional_properties=additional_properties)
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(identifier=2, name='test', type='group',
                                             id=id_node, additional_properties=additional_properties))
        create_node_mock.assert_called_once_with('Activity')
        create_properties_mock.assert_called_once_with(id_node, activity)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_activity_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        activity = ActivityIn(identifier=2)
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(identifier=2, errors=['error']))
        create_node_mock.assert_called_once_with('Activity')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_activity_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        activity = ActivityIn(identifier=2)
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(identifier=2, errors=['error']))
        create_node_mock.assert_called_once_with('Activity')
        create_properties_mock.assert_called_once_with(id_node, activity)
