import unittest
import unittest.mock as mock

from participant.participant_model import *
from models.not_found_model import *

from participant.participant_service_graphdb import ParticipantServiceGraphDB
from graph_api_service import GraphApiService
from participant_state.participant_state_model import BasicParticipantStateOut


class TestParticipantServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    def test_update_participant_without_error(self, delete_node_properties_mock,
                                              get_node_mock, create_properties_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participant'],
                                      'properties': [{'key': 'name', 'value': 'test'},
                                                     {'key': 'sex', 'value': 'male'},
                                                     {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_in = ParticipantIn(name="test", sex='male', additional_properties=additional_properties)
        participant_out = BasicParticipantOut(name="test", sex='male', id=id_node,
                                              additional_properties=additional_properties)
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.update_participant(id_node, participant_in, dataset_name)

        self.assertEqual(result, participant_out)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
        create_properties_mock.assert_called_once_with(id_node, participant_in, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participant_without_participant_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_in = ParticipantIn(name="test", sex='male', id=id_node,
                                       additional_properties=additional_properties)
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.update_participant(id_node, participant_in, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participant_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_in = ParticipantIn(name="test", sex='male', id=id_node,
                                       additional_properties=additional_properties)
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.update_participant(id_node, participant_in, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
