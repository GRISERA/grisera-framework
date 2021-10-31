import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from participant_state.participant_state_model import *
from participant_state.participant_state_service import ParticipantStateService, ParticipantService


def relationship_function(*args, **kwargs):
    if kwargs['name'] == 'hasPublication':
        return {'start_node': 1, 'end_node': 3, 'id': 5, 'name': 'hasPublication', 'errors': ['error']}
    return {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'hasAuthor', 'errors': None}


class TestParticipantStateService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ParticipantService, 'save_participant')
    def test_save_participant_state_without_errors(self, save_participant_mock, create_relationships_mock,
                                                          create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        save_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', identifier=5, id=2)
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        participant = ParticipantIn(name="Test Test", sex='male', identifier=5)
        participant_out = ParticipantOut(name="Test Test", sex='male', identifier=5, id=2)
        participant_state = ParticipantStateIn(participant=participant)
        participant_state_service = ParticipantStateService()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(participant=participant_out, id=1))
        create_node_mock.assert_called_once_with('`Participant State`')
        create_properties_mock.assert_called_once_with(id_node, participant_state)
        save_participant_mock.assert_called_once_with(participant=participant)
        create_relationships_mock.assert_called_once_with(end_node=2, start_node=1, name="hasParticipant")

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participant_state_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participant_state = ParticipantStateIn(participant=ParticipantIn(name="Test Test", sex='male', identifier=5))
        participant_state_service = ParticipantStateService()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(errors=['error']))
        create_node_mock.assert_called_once_with('`Participant State`')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ParticipantService, 'save_participant')
    def test_save_participant_state_with_properties_error(self, save_participant_mock, create_relationships_mock,
                                                          create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        save_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', identifier=5, id=2)
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        participant = ParticipantIn(name="Test Test", sex='male', identifier=5)
        participant_state = ParticipantStateIn(participant=participant)
        participant_state_service = ParticipantStateService()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(errors=['error']))
        create_node_mock.assert_called_once_with('`Participant State`')
        create_properties_mock.assert_called_once_with(id_node, participant_state)
        save_participant_mock.assert_called_once_with(participant=participant)
        create_relationships_mock.assert_called_once_with(end_node=2, start_node=1, name="hasParticipant")
