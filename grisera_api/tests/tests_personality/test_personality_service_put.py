import unittest
import unittest.mock as mock

from personality.personality_model import *
from models.not_found_model import *

from personality.personality_service_graphdb import PersonalityServiceGraphDB
from graph_api_service import GraphApiService


class TestPersonalityServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_personality_big_five_without_error(self, get_node_relationships_mock, get_node_mock,
                                                       create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Personality'],
                                                                      'properties': [
                                                                          {'key': 'agreeableness', 'value': 2.5},
                                                                          {'key': 'conscientiousness', 'value': 2.5},
                                                                          {'key': 'extroversion', 'value': 2.5},
                                                                          {'key': 'neuroticism', 'value': 2.5},
                                                                          {'key': 'openess', 'value': 2.5}],
                                                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        personality_in = PersonalityBigFiveIn(agreeableness=0.5, conscientiousness=0.5, extroversion=0.5,
                                              neuroticism=0.5, openess=0.5)
        personality_out = PersonalityBigFiveOut(agreeableness=0.5, conscientiousness=0.5, extroversion=0.5,
                                                neuroticism=0.5, openess=0.5, id=id_node, relations=[
                                                RelationInformation(second_node_id=19, name="testRelation",
                                                                    relation_id=0)],
                                            reversed_relations=[
                                                RelationInformation(second_node_id=15, name="testReversedRelation",
                                                                    relation_id=0)])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_big_five(id_node, personality_in)

        self.assertEqual(result, personality_out)
        get_node_mock.assert_called_once_with(id_node)
        create_properties_mock.assert_called_once_with(id_node, personality_in)

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_personality_panas_without_error(self, get_node_relationships_mock, get_node_mock,
                                                    create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Personality'],
                                      'properties': [{'key': 'negative_affect', 'value': 0.5},
                                                     {'key': 'positive_affect', 'value': 0.5}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        personality_in = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_out = PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=id_node, relations=[
            RelationInformation(second_node_id=19, name="testRelation",
                                relation_id=0)],
                                          reversed_relations=[
                                              RelationInformation(second_node_id=15, name="testReversedRelation",
                                                                  relation_id=0)])
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_panas(id_node, personality_in)

        self.assertEqual(result, personality_out)
        get_node_mock.assert_called_once_with(id_node)
        create_properties_mock.assert_called_once_with(id_node, personality_in)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_personality_big_five_without_appearance_label(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        personality_in = PersonalityBigFiveIn(agreeableness=0.5, conscientiousness=0.5, extroversion=0.5,
                                              neuroticism=0.5, openess=0.5)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_big_five(id_node, personality_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_personality_panas_without_appearance_label(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        personality_in = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_panas(id_node, personality_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_personality_big_five_with_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        personality_in = PersonalityBigFiveIn(agreeableness=0.5, conscientiousness=0.5, extroversion=0.5,
                                              neuroticism=0.5, openess=0.5)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_big_five(id_node, personality_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_personality_panas_with_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        personality_in = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_panas(id_node, personality_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    def test_update_personality_big_five_with_wrong_range(self):
        id_node = 1
        personality_in = PersonalityBigFiveIn(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                              neuroticism=2.5,
                                              openess=2.5)
        personality_out = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                neuroticism=2.5, openess=2.5, errors="Value not between 0 and 1")
        personality_service = PersonalityServiceGraphDB()

        result = personality_service.update_personality_big_five(id_node, personality_in)

        self.assertEqual(result, personality_out)
