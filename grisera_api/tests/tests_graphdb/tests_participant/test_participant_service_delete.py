import unittest
import unittest.mock as mock

from grisera_api.participant.participant_model import *
from grisera_api.models.not_found_model import *

from grisera_api.participant.participant_service_graphdb import ParticipantServiceGraphDB
from grisera_api.graph_api_service import GraphApiService
from grisera_api.participant_state.participant_state_model import BasicParticipantStateOut


class TestParticipantServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_participant_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Participant'],
                                                                      'properties': [{'key': 'name', 'value': 'test'},
                                                                                     {'key': 'sex', 'value': 'male'},
                                                                                     {'key': 'identifier', 'value': 5}],
                                                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": 19, "end_node": id_node,
                                                     "name": "hasParticipant", "id": 0,
                                                     "properties": None}]}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant = ParticipantOut(name="test", sex='male', id=id_node, additional_properties=additional_properties,
                                     participant_states=[BasicParticipantStateOut(**{id: 19})])
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.delete_participant(id_node)

        self.assertEqual(result, participant)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.delete_participant(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.delete_participant(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
