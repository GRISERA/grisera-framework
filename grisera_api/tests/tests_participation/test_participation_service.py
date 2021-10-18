import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from participation.participation_model import *
from participation.participation_service import ParticipationService


class TestParticipationService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_participant_without_error(self, create_relationships_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_relationships_mock.return_value = {'id': 3, 'start_node': 2, "errors": None, 'links': None}
        calls = [mock.call(id_node, 1, "hasActivity"), mock.call(id_node, 2, "hasParticipantState")]
        participation = ParticipationIn(activity_id=1, participant_state_id=2)
        participation_service = ParticipationService()

        result = participation_service.save_participation(participation)

        self.assertEqual(result, ParticipationOut(activity_id=1, participant_state_id=2, id=id_node))
        create_node_mock.assert_called_once_with('Participation')
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participant_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participation = ParticipationIn(activity_id=1, participant_state_id=2)
        participation_service = ParticipationService()

        result = participation_service.save_participation(participation)

        self.assertEqual(result, ParticipationOut(errors=['error']))
        create_node_mock.assert_called_once_with('Participation')
