import unittest
import unittest.mock as mock

from grisera_api.activity_execution.activity_execution_model import BasicActivityExecutionOut
from grisera_api.participant_state.participant_state_model import BasicParticipantStateOut
from grisera_api.participation.participation_model import *
from grisera_api.models.not_found_model import *

from grisera_api.participation.participation_service_graphdb import ParticipationServiceGraphDB
from grisera_api.graph_api_service import GraphApiService
from grisera_api.recording.recording_model import BasicRecordingOut


class TestParticipationServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_participation_relationships_without_error(self, get_node_relationships_mock,
                                                              delete_node_properties_mock,
                                                              get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
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
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      'properties': None,
                                      "errors": None, 'links': None}
        participation_in = ParticipationIn(activity_execution_id=15, participant_state_id=19)
        participation_out = ParticipationOut(id=id_node, participant_state=BasicParticipantStateOut(**{id: 19}),
                                             activity_execution=BasicActivityExecutionOut(**{id: 15}),
                                             recordings=[BasicRecordingOut(**{id: 16})])
        calls = [mock.call(1)]
        participation_service = ParticipationServiceGraphDB()

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
        participation_in = ParticipationIn(activity_execution_id=15, participant_state_id=19)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.update_participation_relationships(id_node, participation_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participation_relationships_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participation_in = ParticipationIn(activity_execution_id=15, participant_state_id=19)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.update_participation_relationships(id_node, participation_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
