import unittest
import unittest.mock as mock

from participant.participant_model import *
from models.not_found_model import *

from participant.participant_service import ParticipantService
from graph_api_service import GraphApiService


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
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant = ParticipantOut(name="test", sex='male', id=id_node, additional_properties=additional_properties,
                                     relations=
                                     [RelationInformation(second_node_id=19, name="testRelation", relation_id=0)],
                                     reversed_relations=
                                     [RelationInformation(second_node_id=15, name="testReversedRelation", relation_id=0)]
                                     )
        participant_service = ParticipantService()

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
        participant_service = ParticipantService()

        result = participant_service.delete_participant(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participant_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participant_service = ParticipantService()

        result = participant_service.delete_participant(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
