import unittest
import unittest.mock as mock

from participation.participation_model import *
from models.not_found_model import *

from participation.participation_service import ParticipationService
from graph_api_service import GraphApiService


class TestParticipationServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_participation_relationships_without_error(self, get_node_relationships_mock, delete_node_properties_mock,
                                                    get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      'properties': [{'key': 'age', 'value': 5}, {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        participation_in = ParticipationIn(activity_id=15, arrangement_id=19)
        participation_out = ParticipationOut(id=id_node, relations=
                                 [RelationInformation(second_node_id=19, name="testRelation", relation_id=0)],
                                                    reversed_relations=
                                 [RelationInformation(second_node_id=15, name="testReversedRelation", relation_id=0)])
        calls = [mock.call(1)]
        participation_service = ParticipationService()

        result = participation_service.update_participation_relationships(id_node, participation_in)

        self.assertEqual(result, participation_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_not_called()
        get_node_relationships_mock.assert_has_calls([mock.call(1), mock.call(1)])

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participation_relationships_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participation_in = ParticipationIn(activity_id=15, arrangement_id=19)
        participation_service = ParticipationService()

        result = participation_service.update_participation_relationships(id_node, participation_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participation_relationships_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participation_in = ParticipationIn(activity_id=15, arrangement_id=19)
        participation_service = ParticipationService()

        result = participation_service.update_participation_relationships(id_node, participation_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
