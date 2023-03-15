import unittest
import unittest.mock as mock

from grisera_api.participant_state.participant_state_model import BasicParticipantStateOut
from grisera_api.personality.personality_model import *
from grisera_api.models.not_found_model import *

from grisera_api.personality.personality_service_graphdb import PersonalityServiceGraphDB
from grisera_api.graph_api_service import GraphApiService


class TestPersonalityServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_personality_big_five_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Personality'],
                                      'properties': [{'key': 'agreeableness', 'value': 2.5},
                                                     {'key': 'conscientiousness', 'value': 2.5},
                                                     {'key': 'extroversion', 'value': 2.5},
                                                     {'key': 'neuroticism', 'value': 2.5},
                                                     {'key': 'openess', 'value': 2.5}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasPersonality", "id": 0,
             "properties": None}]}
        personality = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5, neuroticism=2.5,
                                            openess=2.5, id=id_node,
                                            participant_states=[BasicParticipantStateOut(**{id: 19})])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.get_personality(id_node)

        self.assertEqual(result, personality)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_personality_panas_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Personality'],
                                      'properties': [{'key': 'negative_affect', 'value': 0.5},
                                                     {'key': 'positive_affect', 'value': 0.5}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasPersonality", "id": 0,
             "properties": None}]}
        personality = PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=id_node,
                                          participant_states=[BasicParticipantStateOut(**{id: 19})])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.get_personality(id_node)

        self.assertEqual(result, personality)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_personality_without_appearance_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.get_personality(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_personality_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.get_personality(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_personalities(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Personality'],
                                                  'properties': [{'key': 'agreeableness', 'value': 2.5},
                                                                 {'key': 'conscientiousness', 'value': 2.5},
                                                                 {'key': 'extroversion', 'value': 2.5},
                                                                 {'key': 'neuroticism', 'value': 2.5},
                                                                 {'key': 'openess', 'value': 2.5}]},
                                                 {'id': 2, 'labels': ['Personality'],
                                                  'properties': [{'key': 'negative_affect', 'value': 0.5},
                                                                 {'key': 'positive_affect', 'value': 0.5}]}]}
        personality_big_five = BasicPersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                          neuroticism=2.5, openess=2.5, id=1)
        personality_panas = BasicPersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=2)
        personalities = PersonalitiesOut(personalities=[personality_big_five, personality_panas])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.get_personalities()

        self.assertEqual(result, personalities)
        get_nodes_mock.assert_called_once_with("Personality")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_personalities_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        personalities = PersonalitiesOut(personality=[])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.get_personalities()

        self.assertEqual(result, personalities)
        get_nodes_mock.assert_called_once_with("Personality")
