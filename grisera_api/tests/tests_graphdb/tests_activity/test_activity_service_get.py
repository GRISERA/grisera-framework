import unittest
import unittest.mock as mock

from activity.activity_model import *
from activity.activity_service_graphdb import ActivityServiceGraphDB
from activity_execution.activity_execution_model import BasicActivityExecutionOut
from graph_api_service import GraphApiService
from models.not_found_model import *
from services import Services


class TestActivityServiceGet(unittest.TestCase):
    """TODO: expand unit test for get with depth different from  0"""

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_activity_without_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Activity'],
                                      'properties': [{'key': 'activity', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        activity = BasicActivityOut(activity="test", id=id_node, additional_properties=[{'key': 'test',
                                                                                         'value': 'test'}])
        activity_service = ActivityServiceGraphDB()

        result = activity_service.get_activity(id_node,dataset_name)

        self.assertEqual(result, activity)
        get_node_mock.assert_called_once_with(id_node,dataset_name)



    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_activity_without_participant_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        activity_service = ActivityServiceGraphDB()

        result = activity_service.get_activity(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_activity_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        activity_service = ActivityServiceGraphDB()

        result = activity_service.get_activity(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_activities(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Activity'],
                                                  'properties': [{'key': 'activity', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Activity'],
                                                  'properties': [{'key': 'activity', 'value': 'test2'}]}],
                                       'errors': None}
        activity_one = BasicActivityOut(activity="test", id=1)
        activity_two = BasicActivityOut(activity="test2", id=2)
        activities = ActivitiesOut(activities=[activity_one, activity_two])
        activity_service = ActivityServiceGraphDB()

        result = activity_service.get_activities(dataset_name)

        self.assertEqual(result, activities)
        get_nodes_mock.assert_called_once_with("Activity", dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_activities_empty(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        activities = ActivitiesOut(activities=[])
        activity_service = Services().activity_service()

        result = activity_service.get_activities(dataset_name)

        self.assertEqual(result, activities)
        get_nodes_mock.assert_called_once_with("Activity", dataset_name)
