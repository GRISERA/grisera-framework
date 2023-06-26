import unittest
import unittest.mock as mock

from appearance.appearance_model import BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from graph_api_service import GraphApiService
from participant.participant_model import BasicParticipantOut, Sex
from participant.participant_service_graphdb import ParticipantServiceGraphDB
from participant_state.participant_state_model import *
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from participation.participation_model import BasicParticipationOut
from personality.personality_model import BasicPersonalityPanasOut, BasicPersonalityBigFiveOut
from personality.personality_service_graphdb import PersonalityServiceGraphDB


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
    @mock.patch.object(ParticipantServiceGraphDB, 'get_participant')
    @mock.patch.object(PersonalityServiceGraphDB, 'get_personality')
    @mock.patch.object(AppearanceServiceGraphDB, 'get_appearance')
    def test_save_participant_state_without_errors(self, get_appearance_mock, get_personality_mock, get_participant_mock, get_node_relationships_mock, get_node_mock,
                                                   create_relationships_mock, create_properties_mock, create_node_mock):
        id_node = 1
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_state_in = ParticipantStateIn(age=12, additional_properties=additional_properties, participant_id=6, personality_ids=[7,8], appearance_ids=[9,10])
        participant_state_out = BasicParticipantStateOut(id=id_node, age=12, additional_properties=additional_properties)

        create_node_mock.return_value = {'id': id_node, 'labels': ['Participant State'],
                                         'properties': [],
                                         "errors": None, 'links': None}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participant State'],
                                      'properties': [{'key': 'age', 'value': 12},
                                                     {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}

        participant_state_service = ParticipantStateServiceGraphDB()

        participant_state_service.participant_service = mock.create_autospec(ParticipantServiceGraphDB)
        get_participant_mock.return_value = BasicParticipantOut(id=6, name='testowy', sex=Sex.female)
        participant_state_service.participant_service.get_participant = get_participant_mock

        participant_state_service.personality_service = mock.create_autospec(PersonalityServiceGraphDB)
        get_personality_mock.return_value = BasicPersonalityBigFiveOut(id=7, agreeableness=1.5, conscientiousness=1.5,
                                                                       extroversion=1.5, neuroticism=1.5, openess=1.5)
        participant_state_service.personality_service.get_personality = get_personality_mock

        participant_state_service.appearance_service = mock.create_autospec(AppearanceServiceGraphDB)
        get_appearance_mock.return_value = BasicAppearanceSomatotypeOut(id=8, ectomorph=1.5, endomorph=1.0,
                                                                        mesomorph=1.0)
        participant_state_service.appearance_service.get_appearance = get_appearance_mock

        result = participant_state_service.save_participant_state(participant_state_in)

        create_relationships_mock.assert_has_calls([mock.call(start_node=id_node, end_node=6, name="hasParticipant"),
                                                    mock.call(start_node=id_node, end_node=7, name="hasPersonality"),
                                                    mock.call(start_node=id_node, end_node=8, name="hasPersonality"),
                                                    mock.call(start_node=id_node, end_node=9, name="hasAppearance"),
                                                    mock.call(start_node=id_node, end_node=10, name="hasAppearance")])
        create_properties_mock.assert_called_once_with(id_node, participant_state_in)
        get_node_mock.assert_called_once_with(id_node)
        self.assertEqual(result, participant_state_out)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participant_state_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participant_state = ParticipantStateIn(age=5, participant_id=1, personality_id=2)
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(age=5, errors=['error']))
        create_node_mock.assert_called_once_with('Participant State')
