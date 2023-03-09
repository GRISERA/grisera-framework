import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from participation.participation_model import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB


class TestParticipationServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_participation_without_errors(self, get_node_relationships_mock, get_node_mock,
                                                    create_relationships_mock, create_properties_mock,
                                                    create_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      'properties': None,
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
                                                  'name': 'hasActivityExecution', 'errors': None}

        participation_in = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_out = ParticipationOut(relations=[RelationInformation(second_node_id=19,
                                                                            name="testRelation",
                                                                            relation_id=0)],
                                             reversed_relations=[RelationInformation(second_node_id=15,
                                                                                     name="testReversedRelation",
                                                                                     relation_id=0)], id=id_node)
        calls = [mock.call(2, database_name), mock.call(3, database_name), mock.call(1, database_name)]
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.save_participation(participation_in, database_name)

        self.assertEqual(result, participation_out)
        create_node_mock.assert_called_once_with('Participation', database_name)
        # create_properties_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participation_with_node_error(self, create_node_mock):
        database_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participation = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.save_participation(participation, database_name)

        self.assertEqual(result, ParticipationOut(errors=['error']))
        create_node_mock.assert_called_once_with('Participation', database_name)
