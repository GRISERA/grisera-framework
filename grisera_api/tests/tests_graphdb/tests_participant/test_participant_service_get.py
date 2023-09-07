import unittest
import unittest.mock as mock

from participant.participant_model import *
from models.not_found_model import *

from participant.participant_service_graphdb import ParticipantServiceGraphDB
from graph_api_service import GraphApiService
from participant_state.participant_state_model import BasicParticipantStateOut


class TestParticipantServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participant_without_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participant'],
                                      'properties': [{'key': 'name', 'value': 'test'},
                                                     {'key': 'sex', 'value': 'male'},
                                                     {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant = BasicParticipantOut(name="test", sex='male', id=id_node, additional_properties=additional_properties)
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.get_participant(id_node, dataset_name)

        self.assertEqual(result, participant)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_get_participant_without_error(self, get_node_relationships_mock, get_node_mock):
    #     id_node = 1
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Participant'],
    #                                   'properties': [{'key': 'name', 'value': 'test'},
    #                                                  {'key': 'sex', 'value': 'male'},
    #                                                  {'key': 'identifier', 'value': 5}],
    #                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": 19, "end_node": id_node,
    #          "name": "hasParticipant", "id": 0,
    #          "properties": None}]}
    #     additional_properties = [PropertyIn(key='identifier', value=5)]
    #     participant = ParticipantOut(name="test", sex='male', id=id_node, additional_properties=additional_properties,
    #                                  participant_states=[BasicParticipantStateOut(**{id: 19})])
    #     participant_service = ParticipantServiceGraphDB()
    #
    #     result = participant_service.get_participant(id_node)
    #
    #     self.assertEqual(result, participant)
    #     get_node_mock.assert_called_once_with(id_node)
    #     get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participant_without_participant_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.get_participant(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participant_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.get_participant(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_participants(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Participant'],
                                                  'properties': [{'key': 'name', 'value': 'test'},
                                                                 {'key': 'sex', 'value': 'male'}]},
                                                 {'id': 2, 'labels': ['Participant'],
                                                  'properties': [{'key': 'name', 'value': 'test2'},
                                                                 {'key': 'sex', 'value': 'female'}]}]}
        participant_one = BasicParticipantOut(id=1, name="test", sex="male", additional_properties=[])
        participant_two = BasicParticipantOut(id=2, name="test2", sex="female", additional_properties=[])
        participants = ParticipantsOut(participants=[participant_one, participant_two])
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.get_participants(dataset_name)

        self.assertEqual(result, participants)
        get_nodes_mock.assert_called_once_with("Participant", dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_participants_empty(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': []}
        participants = ParticipantsOut(participant=[])
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.get_participants(dataset_name)

        self.assertEqual(result, participants)
        get_nodes_mock.assert_called_once_with("Participant", dataset_name)
