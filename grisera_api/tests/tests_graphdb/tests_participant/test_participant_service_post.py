import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from participant.participant_model import *
from participant.participant_service_graphdb import ParticipantServiceGraphDB


class TestParticipantServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_participant_without_error(self, create_properties_mock, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'sex', 'value': 'male'},
                                                                             {'key': 'identifier', 'value': 5}],
                                               "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]
        participant = ParticipantIn(name="Test Test", sex='male', additional_properties=additional_properties)
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.save_participant(participant, dataset_name)

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', id=id_node,
                                                additional_properties=additional_properties))
        create_node_mock.assert_called_once_with('Participant', dataset_name)
        create_properties_mock.assert_called_once_with(id_node, participant, dataset_name)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participant_with_node_error(self, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participant = ParticipantIn(name="Test Test", sex='male',)
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.save_participant(participant, dataset_name)

        self.assertEqual(result, ParticipantOut(sex='male', name="Test Test", errors=['error']))
        create_node_mock.assert_called_once_with('Participant', dataset_name)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_participant_with_properties_error(self, create_properties_mock, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        participant = ParticipantIn(name="Test Test", sex='male')
        participant_service = ParticipantServiceGraphDB()

        result = participant_service.save_participant(participant, dataset_name)

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', errors=['error']))
        create_node_mock.assert_called_once_with('Participant', dataset_name)
        create_properties_mock.assert_called_once_with(id_node, participant, dataset_name)
