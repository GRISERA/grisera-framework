import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import BasicActivityExecutionOut
from graph_api_service import GraphApiService
from participant_state.participant_state_model import BasicParticipantStateOut
from participation.participation_model import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from recording.recording_model import BasicRecordingOut


class TestParticipationServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_participation_without_errors(self, get_node_relationships_mock, get_node_mock,
                                                    create_relationships_mock, create_properties_mock,
                                                    create_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      'properties': None,
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
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasActivityExecution', 'errors': None}

        participation_in = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_out = ParticipationOut(id=id_node, participant_state=BasicParticipantStateOut(**{id: 19}),
                                         activity_execution=BasicActivityExecutionOut(**{id: 15}),
                                         recordings=[BasicRecordingOut(**{id: 16})])
        calls = [mock.call(2), mock.call(3), mock.call(1)]
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.save_participation(participation_in)

        self.assertEqual(result, participation_out)
        create_node_mock.assert_called_once_with('Participation')
        # create_properties_mock.assert_not_called()
        create_relationships_mock.assert_not_called()
        get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participation_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participation = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.save_participation(participation)

        self.assertEqual(result, ParticipationOut(errors=['error']))
        create_node_mock.assert_called_once_with('Participation')
