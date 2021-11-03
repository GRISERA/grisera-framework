import unittest
import unittest.mock as mock

from live_activity.live_activity_model import *
from models.not_found_model import *

from live_activity.live_activity_service import LiveActivityService
from graph_api_service import GraphApiService


class TestLiveActivityServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_live_activity_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Live Activity'],
                                      'properties': [{'key': 'live_activity', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        live_activity = LiveActivityOut(live_activity="test", id=id_node,
                                   relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                  relation_id=0)],
                                   reversed_relations=[RelationInformation(second_node_id=15,
                                                                           name="testReversedRelation", relation_id=0)])
        live_activity_service = LiveActivityService()

        result = live_activity_service.get_live_activity(id_node)

        self.assertEqual(result, live_activity)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_live_activity_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        live_activity_service = LiveActivityService()

        result = live_activity_service.get_live_activity(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_live_activity_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        live_activity_service = LiveActivityService()

        result = live_activity_service.get_live_activity(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_live_activities(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Live Activity'],
                                                  'properties': [{'key': 'live_activity', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Live Activity'],
                                                  'properties': [{'key': 'live_activity', 'value': 'test2'}]}],
                                       'errors': None}
        live_activity_one = BasicLiveActivityOut(live_activity="test", id=1)
        live_activity_two = BasicLiveActivityOut(live_activity="test2", id=2)
        live_activities = LiveActivitiesOut(live_activities=[live_activity_one, live_activity_two])
        live_activity_service = LiveActivityService()

        result = live_activity_service.get_live_activities()

        self.assertEqual(result, live_activities)
        get_nodes_mock.assert_called_once_with("`Live Activity`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_live_activities_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        live_activities = LiveActivitiesOut(live_activities=[])
        live_activity_service = LiveActivityService()

        result = live_activity_service.get_live_activities()

        self.assertEqual(result, live_activities)
        get_nodes_mock.assert_called_once_with("`Live Activity`")
