import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from participant_state.participant_state_model import *
from participant_state.participant_state_service import ParticipantStateService, ParticipantService


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
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasParticipant', 'errors': None}
        participant_state_in = ParticipantStateIn(age=5, participant_id=2, personality_id=3)
        participant_state_out = ParticipantStateOut(age=5, additional_properties=[PropertyIn(key='test',
                                                                                             value='test2')],
                                                    relations=
                                                    [RelationInformation(second_node_id=19, name="testRelation",
                                                                         relation_id=0)],
                                                    reversed_relations=
                                                    [RelationInformation(second_node_id=15, name="testReversedRelation",
                                                                         relation_id=0)], id=1)
        calls = [mock.call(end_node=3, start_node=1, name="hasPersonality")]
        participant_state_service = ParticipantStateService()

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
        participant_state_service = ParticipantStateService()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(age=5, errors=['error']))
        create_node_mock.assert_called_once_with('`Participant State`')
