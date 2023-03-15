import unittest
import unittest.mock as mock

from grisera_api.activity_execution.activity_execution_model import BasicActivityExecutionOut
from grisera_api.graph_api_service import GraphApiService
from grisera_api.models.not_found_model import *
from grisera_api.participant_state.participant_state_model import BasicParticipantStateOut
from grisera_api.participation.participation_model import *
from grisera_api.participation.participation_service_graphdb import ParticipationServiceGraphDB
from grisera_api.recording.recording_model import BasicRecordingOut


class TestParticipationServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_participation_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "hasParticipantState", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 15,
             "name": "hasActivityExecution", "id": 0,
             "properties": None},
            {"start_node": 16, "end_node": id_node,
             "name": "hasParticipation", "id": 0,
             "properties": None},
        ]}
        participation = ParticipationOut(id=id_node, participant_state=BasicParticipantStateOut(**{id: 19}),
                                         activity_execution=BasicActivityExecutionOut(**{id: 15}),
                                         recordings=[BasicRecordingOut(**{id: 16})])
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.get_participation(id_node)

        self.assertEqual(result, participation)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participation_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.get_participation(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_participation_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.get_participation(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_participations(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Participation'],
                                                  'properties': None},
                                                 {'id': 2, 'labels': ['Participation'],
                                                  'properties': None
                                                  }]}

        participation_one = BasicParticipationOut(id=1)
        participation_two = BasicParticipationOut(id=2)
        participations = ParticipationsOut(
            participations=[participation_one, participation_two])
        participations_service = ParticipationServiceGraphDB()

        result = participations_service.get_participations()

        self.assertEqual(result, participations)
        get_nodes_mock.assert_called_once_with("Participation")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_participations_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        participations = ParticipationsOut(participation=[])
        participations_service = ParticipationServiceGraphDB()

        result = participations_service.get_participations()

        self.assertEqual(result, participations)
        get_nodes_mock.assert_called_once_with("Participation")
