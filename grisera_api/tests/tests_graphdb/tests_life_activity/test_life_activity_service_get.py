import unittest
import unittest.mock as mock

from life_activity.life_activity_model import *
from models.not_found_model import *

from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from graph_api_service import GraphApiService


class TestLifeActivityServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_life_activity_without_error(self, get_node_relationships_mock, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Life Activity'],
                                      'properties': [{'key': 'life_activity', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        life_activity = LifeActivityOut(life_activity="test", id=id_node,
                                   relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                  relation_id=0)],
                                   reversed_relations=[RelationInformation(second_node_id=15,
                                                                           name="testReversedRelation", relation_id=0)])
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.get_life_activity(id_node, database_name)

        self.assertEqual(result, life_activity)
        get_node_mock.assert_called_once_with(id_node, database_name)
        get_node_relationships_mock.assert_called_once_with(id_node, database_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_life_activity_without_participant_label(self, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.get_life_activity(id_node, database_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, database_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_life_activity_with_error(self, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.get_life_activity(id_node, database_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, database_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_life_activities(self, get_nodes_mock):
        database_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Life Activity'],
                                                  'properties': [{'key': 'life_activity', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Life Activity'],
                                                  'properties': [{'key': 'life_activity', 'value': 'test2'}]}],
                                       'errors': None}
        life_activity_one = BasicLifeActivityOut(life_activity="test", id=1)
        life_activity_two = BasicLifeActivityOut(life_activity="test2", id=2)
        life_activities = LifeActivitiesOut(life_activities=[life_activity_one, life_activity_two])
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.get_life_activities(database_name)

        self.assertEqual(result, life_activities)
        get_nodes_mock.assert_called_once_with("`Life Activity`", database_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_life_activities_empty(self, get_nodes_mock):
        database_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        life_activities = LifeActivitiesOut(life_activities=[])
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.get_life_activities(database_name)

        self.assertEqual(result, life_activities)
        get_nodes_mock.assert_called_once_with("`Life Activity`", database_name)
