import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import BasicActivityExecutionOut
from graph_api_service import GraphApiService
from models.not_found_model import *
from participant_state.participant_state_model import BasicParticipantStateOut
from participation.participation_model import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from recording.recording_model import BasicRecordingOut


class TestParticipationServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participation_without_error(self, get_node_mock,
                                                delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Participation'],
                                                                      'properties': None,
                                                                      "errors": None, 'links': None}
        participation = BasicParticipationOut(id=id_node)
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.delete_participation(id_node)

        self.assertEqual(result, participation)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participation_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.delete_participation(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_participation_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        participation_service = ParticipationServiceGraphDB()

        result = participation_service.delete_participation(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
