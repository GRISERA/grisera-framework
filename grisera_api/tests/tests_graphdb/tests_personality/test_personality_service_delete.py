import unittest
import unittest.mock as mock

from participant_state.participant_state_model import BasicParticipantStateOut
from personality.personality_model import *
from models.not_found_model import *

from personality.personality_service_graphdb import PersonalityServiceGraphDB
from graph_api_service import GraphApiService


class TestPersonalityServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_personality_big_five_without_error(self, get_node_mock,
                                                       delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Personality'],
                                                                      'properties': [
                                                                          {'key': 'agreeableness', 'value': 2.5},
                                                                          {'key': 'conscientiousness', 'value': 2.5},
                                                                          {'key': 'extroversion', 'value': 2.5},
                                                                          {'key': 'neuroticism', 'value': 2.5},
                                                                          {'key': 'openess', 'value': 2.5}],
                                                                      'errors': None, 'links': None}
        personality = BasicPersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                 neuroticism=2.5,
                                                 openess=2.5, id=id_node)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.delete_personality(id_node)

        self.assertEqual(result, personality)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_personality_panas_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Personality'],
                                                                      'properties': [
                                                                          {'key': 'negative_affect', 'value': 0.5},
                                                                          {'key': 'positive_affect', 'value': 0.5}],
                                                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasPersonality", "id": 0,
             "properties": None}]}
        personality = BasicPersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=id_node)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.delete_personality(id_node)

        self.assertEqual(result, personality)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_personality_without_personality_label(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasPersonality", "id": 0,
             "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.delete_personality(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_personality_with_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasPersonality", "id": 0,
             "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.delete_personality(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
