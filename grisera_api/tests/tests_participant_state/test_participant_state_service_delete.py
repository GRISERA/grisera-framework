import unittest
import unittest.mock as mock

from participant_state.participant_state_model import *
from models.not_found_model import *

from participant_state.participant_state_service import ParticipantStateService
from graph_api_service import GraphApiService


class TestParticipantStateServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_state_without_error(self, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Participant State'],
                                                                      'properties': [{'key': 'age', 'value': 5}],
                                                                      "errors": None, 'links': None}
        participant_state = ParticipantStateOut(age=5, id=id_node, additional_properties=[])
        participant_state_service = ParticipantStateService()

        result = participant_state_service.delete_participant_state(id_node)

        self.assertEqual(result, participant_state)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_state_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participant_state_service = ParticipantStateService()

        result = participant_state_service.delete_participant_state(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_state_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participant_state_service = ParticipantStateService()

        result = participant_state_service.delete_participant_state(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
