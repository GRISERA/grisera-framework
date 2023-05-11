import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import BasicActivityExecutionOut
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from graph_api_service import GraphApiService
from participant_state.participant_state_model import BasicParticipantStateOut
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from participation.participation_model import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB


class TestParticipationServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(ActivityExecutionServiceGraphDB, 'get_activity_execution')
    @mock.patch.object(ParticipantStateServiceGraphDB, 'get_participant_state')
    def test_save_participation_without_errors(self, get_participant_state_mock, get_activity_execution_mock,
                                               get_node_mock,
                                               create_relationships_mock, create_properties_mock,
                                               create_node_mock):
        id_node = 1
        dataset_name = "neo4j"
        participation_in = ParticipationIn(activity_execution_id=6, participant_state_id=7)
        participation_out = BasicParticipationOut(id=id_node)

        create_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                         'properties': [],
                                         "errors": None, 'links': None}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      "errors": None, 'links': None}

        participation_service = ParticipationServiceGraphDB()

        participation_service.activity_execution_service = mock.create_autospec(ActivityExecutionServiceGraphDB)
        get_activity_execution_mock.return_value = BasicActivityExecutionOut(id=6)
        participation_service.activity_execution_service.get_activity_execution = get_activity_execution_mock

        participation_service.participant_state_service = mock.create_autospec(ParticipantStateServiceGraphDB)
        get_participant_state_mock.return_value = BasicParticipantStateOut(id=7, age=15, additional_properties=[])
        participation_service.participant_state_service.get_participant_state = get_participant_state_mock

        result = participation_service.save_participation(participation_in,dataset_name)


        create_relationships_mock.assert_has_calls(
            [mock.call(start_node=id_node, end_node=6, name="hasActivityExecution"),
             mock.call(start_node=id_node, end_node=7, name="hasParticipantState")])
        create_properties_mock.assert_not_called()
        get_node_mock.assert_called_once_with(id_node)
        self.assertEqual(result, participation_out)


    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_participation_with_node_error(self, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        participation = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.save_participation(participation, dataset_name)

        self.assertEqual(result, ParticipationOut(errors=['error']))
        create_node_mock.assert_called_once_with('Participation', dataset_name)
