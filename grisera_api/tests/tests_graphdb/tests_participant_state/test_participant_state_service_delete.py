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


class BasicAppearanceOut:
    pass


class BasicPersonalityOut:
    pass


class TestParticipantStateServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_state_without_error(self, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Participant State'],
                                                                      'properties': [{'key': 'age', 'value': 5}],
                                                                      "errors": None, 'links': None}
        participant_state = BasicParticipantStateOut(age=5, id=id_node, additional_properties=[])
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.delete_participant_state(id_node)

        self.assertEqual(result, participant_state)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    # @mock.patch.object(GraphApiService, 'delete_node')
    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_delete_participant_state_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
    #     id_node = 1
    #     delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Participant State'],
    #                                                                   'properties': [{'key': 'age', 'value': 5}],
    #                                                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": 19, "end_node": id_node,
    #          "name": "hasParticipantState", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 15,
    #          "name": "hasParticipant", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 16,
    #          "name": "hasAppearance", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 26,
    #          "name": "hasAppearance", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 17,
    #          "name": "hasPersonality", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 27,
    #          "name": "hasPersonality", "id": 0,
    #          "properties": None},
    #     ]}
    #     participant_state = ParticipantStateOut(age=5, id=id_node, additional_properties=[],
    #                                             participations=[BasicParticipationOut(**{id: 19})],
    #                                             participant=BasicParticipantOut(**{id: 15}),
    #                                             appearances=[BasicAppearanceSomatotypeOut(**{id: 16}),
    #                                                          BasicAppearanceOcclusionOut(**{id: 26})],
    #                                             personalities=[BasicPersonalityPanasOut(**{id: 17}),
    #                                                            BasicPersonalityBigFiveOut(**{id: 27})])
    #     participant_state_service = ParticipantStateServiceGraphDB()
    #
    #     result = participant_state_service.delete_participant_state(id_node)
    #
    #     self.assertEqual(result, participant_state)
    #     get_node_mock.assert_called_once_with(id_node)
    #     delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_state_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.delete_participant_state(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_state_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.delete_participant_state(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
