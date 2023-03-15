import unittest
import unittest.mock as mock

from appearance.appearance_model import BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut
from participant.participant_model import BasicParticipantOut
from participant_state.participant_state_model import *
from models.not_found_model import *

from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from graph_api_service import GraphApiService
from participation.participation_model import BasicParticipationOut
from personality.personality_model import BasicPersonalityPanasOut, BasicPersonalityBigFiveOut


class TestParticipantStateServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_participant_state_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participant State'],
                                      'properties': [{'key': 'age', 'value': 5},
                                                     {'key': 'test', 'value': 'test2'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasParticipantState", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 15,
             "name": "hasParticipant", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 16,
             "name": "hasAppearance", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 26,
             "name": "hasAppearance", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 17,
             "name": "hasPersonality", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 27,
             "name": "hasPersonality", "id": 0,
             "properties": None},
        ]}
        participant_state = ParticipantStateOut(age=5, id=id_node, additional_properties=[],
                                                participations=[BasicParticipationOut(**{id: 19})],
                                                participant=BasicParticipantOut(**{id: 15}),
                                                appearances=[BasicAppearanceSomatotypeOut(**{id: 16}),
                                                             BasicAppearanceOcclusionOut(**{id: 26})],
                                                personalities=[BasicPersonalityPanasOut(**{id: 17}),
                                                               BasicPersonalityBigFiveOut(**{id: 27})])
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.get_participant_state(id_node)

        self.assertEqual(result, participant_state)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participant_state_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.get_participant_state(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participant_state_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.get_participant_state(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_participant_states(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Participant State'],
                                                  'properties': [{'key': 'age', 'value': 5},
                                                                 {'key': 'test', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Participant'],
                                                  'properties': [{'key': 'age', 'value': 10},
                                                                 {'key': 'test2', 'value': 'test3'}]}]}
        participant_state_one = BasicParticipantStateOut(id=1, age=5, additional_properties=[
            PropertyIn(key='test', value='test')])
        participant_state_two = BasicParticipantStateOut(id=2, age=10, additional_properties=[
            PropertyIn(key='test2', value='test3')])
        participant_states = ParticipantStatesOut(participant_states=[participant_state_one, participant_state_two])
        participant_states_service = ParticipantStateServiceGraphDB()

        result = participant_states_service.get_participant_states()

        self.assertEqual(result, participant_states)
        get_nodes_mock.assert_called_once_with("`Participant State`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_participant_states_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        participant_states = ParticipantStatesOut(participant_state=[])
        participant_states_service = ParticipantStateServiceGraphDB()

        result = participant_states_service.get_participant_states()

        self.assertEqual(result, participant_states)
        get_nodes_mock.assert_called_once_with("`Participant State`")
