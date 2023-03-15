import unittest
import unittest.mock as mock

from grisera_api.personality.personality_model import *
from grisera_api.personality.personality_service_graphdb import PersonalityServiceGraphDB
from grisera_api.graph_api_service import GraphApiService


class TestPersonalityServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_personality_big_five_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'agreeableness', 'value': 0.5},
                                                                             {'key': 'conscientiousness', 'value': 0.5},
                                                                             {'key': 'extroversion', 'value': 0.5},
                                                                             {'key': 'neuroticism', 'value': 0.5},
                                                                             {'key': 'openess', 'value': 0.5}],
                                               "errors": None, 'links': None}
        personality = PersonalityBigFiveIn(agreeableness=0.5, conscientiousness=0.5, extroversion=0.5,
                                           neuroticism=0.5, openess=0.5)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.save_personality_big_five(personality)

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=0.5, conscientiousness=0.5, extroversion=0.5,
                                                       neuroticism=0.5, openess=0.5, id=id_node))
        create_node_mock.assert_called_once_with('Personality')
        create_properties_mock.assert_called_once_with(id_node, personality)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_personality_panas_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'negative_affect', 'value': 0.5},
                                                                             {'key': 'positive_affect', 'value': 0.5}],
                                               "errors": None, 'links': None}
        personality = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.save_personality_panas(personality)

        self.assertEqual(result, PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=id_node))
        create_node_mock.assert_called_once_with('Personality')
        create_properties_mock.assert_called_once_with(id_node, personality)
