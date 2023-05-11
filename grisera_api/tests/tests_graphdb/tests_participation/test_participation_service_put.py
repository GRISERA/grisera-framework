import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import BasicActivityExecutionOut
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from participant_state.participant_state_model import BasicParticipantStateOut
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from participation.participation_model import *
from models.not_found_model import *

from participation.participation_service_graphdb import ParticipationServiceGraphDB
from graph_api_service import GraphApiService
from recording.recording_model import BasicRecordingOut


class TestParticipationServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'get_node_relationships')

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'get_activity_execution')
    @mock.patch.object(ParticipantStateServiceGraphDB, 'get_participant_state')
    def test_update_participation_relationships_without_error(self, get_activity_execution_mock,
                                                              get_participant_state_mock, get_node_relationships_mock,
                                                              delete_node_properties_mock, create_relationships_mock,
                                                              get_node_mock, create_properties_mock):

        id_node = 1
        dataset_name = "neo4j"
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}

        get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                      'properties': None,
                                      "errors": None, 'links': None}

        participation_in = ParticipationIn(activity_execution_id=6, participant_state_id=7)
        participation_out = BasicParticipationOut(id=id_node)
        calls = [mock.call(1,dataset_name)]
        participation_service = ParticipationServiceGraphDB()

        participation_service.activity_execution_service = mock.create_autospec(ActivityExecutionServiceGraphDB)
        get_activity_execution_mock.return_value = BasicActivityExecutionOut(id=6)
        participation_service.activity_execution_service.get_activity_execution = get_activity_execution_mock

        participation_service.participant_state_service = mock.create_autospec(ParticipantStateServiceGraphDB)
        get_participant_state_mock.return_value = BasicParticipantStateOut(id=7, age=15, additional_properties=[])
        participation_service.participant_state_service.get_participant_state = get_participant_state_mock

        result = participation_service.update_participation_relationships(id_node, participation_in,dataset_name)


        create_relationships_mock.assert_has_calls([mock.call(start_node=id_node, end_node=6,
                                                              name="hasActivityExecution",dataset_name=dataset_name),
                                                    mock.call(start_node=id_node, end_node=7,
                                                              name="hasParticipantState",dataset_name=dataset_name)])
        self.assertEqual(result, participation_out)


    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participation_relationships_without_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participation_in = ParticipationIn(activity_execution_id=15, participant_state_id=19)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.update_participation_relationships(id_node, participation_in, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)


    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participation_relationships_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participation_in = ParticipationIn(activity_execution_id=15, participant_state_id=19)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.update_participation_relationships(id_node, participation_in, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
