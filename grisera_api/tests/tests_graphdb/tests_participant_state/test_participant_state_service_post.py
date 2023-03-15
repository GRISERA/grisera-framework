import unittest
import unittest.mock as mock

from grisera_api.appearance.appearance_model import BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut
from grisera_api.graph_api_service import GraphApiService
from grisera_api.participant.participant_model import BasicParticipantOut
from grisera_api.participant_state.participant_state_model import *
from grisera_api.participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from grisera_api.participation.participation_model import BasicParticipationOut
from grisera_api.personality.personality_model import BasicPersonalityPanasOut, BasicPersonalityBigFiveOut


def relationship_function(*args, **kwargs):
    if kwargs['name'] == 'hasPublication':
        return {'start_node': 1, 'end_node': 3, 'id': 5, 'name': 'hasPublication', 'errors': ['error']}
    return {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'hasAuthor', 'errors': None}


class TestParticipantStateServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_participant_state_without_errors(self, get_node_relationships_mock, get_node_mock,
                                                   create_relationships_mock, create_properties_mock, create_node_mock):
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
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        participant_state_in = ParticipantStateIn(age=5, participant_id=2, personality_id=3)
        participant_state_out = ParticipantStateOut(age=5, id=id_node, additional_properties=[],
                                                    participations=[BasicParticipationOut(**{id: 19})],
                                                    participant=BasicParticipantOut(**{id: 15}),
                                                    appearances=[BasicAppearanceSomatotypeOut(**{id: 16}),
                                                                 BasicAppearanceOcclusionOut(**{id: 26})],
                                                    personalities=[BasicPersonalityPanasOut(**{id: 17}),
                                                                   BasicPersonalityBigFiveOut(**{id: 27})])
        calls = [mock.call(end_node=3, start_node=1, name="hasPersonality")]
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.save_participant_state(participant_state_in)

        self.assertEqual(result, participant_state_out)
        create_node_mock.assert_called_once_with('`Participant State`')
        create_properties_mock.assert_called_once_with(id_node, participant_state_in)
        create_relationships_mock.assert_not_called()

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participant_state_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participant_state = ParticipantStateIn(age=5, participant_id=1, personality_id=2)
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(age=5, errors=['error']))
        create_node_mock.assert_called_once_with('`Participant State`')
