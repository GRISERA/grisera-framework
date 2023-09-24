import unittest
import unittest.mock as mock

from appearance.appearance_model import BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut
from participant.participant_model import BasicParticipantOut
from participant_state.participant_state_model import *
from models.not_found_model import *

from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from graph_api_service import GraphApiService
from participation.participation_model import BasicParticipationOut
from personality.personality_model import BasicPersonalityPanasOut, BasicPersonalityBigFiveOut


class TestParticipantStateServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    def test_update_participant_state_without_error(self, delete_node_properties_mock,
                                                    get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Participant_State'],
                                      'properties': [{'key': 'age', 'value': 12},
                                                     {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_state_in = ParticipantStateIn(age=12, additional_properties=additional_properties)
        participant_state_out = BasicParticipantStateOut(age=12, id=id_node,
                                                         additional_properties=additional_properties)
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.update_participant_state(id_node, participant_state_in)

        self.assertEqual(result, participant_state_out)
        get_node_mock.assert_called_once_with(id_node)
        create_properties_mock.assert_called_once_with(id_node, participant_state_in)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participant_state_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_state_in = ParticipantStatePropertyIn(age=5, id=id_node,
                                                          additional_properties=additional_properties)
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.update_participant_state(id_node, participant_state_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_participant_state_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        additional_properties = [PropertyIn(key='identifier', value=5)]
        participant_state_in = ParticipantStatePropertyIn(age=5, id=id_node,
                                                          additional_properties=additional_properties)
        participant_state_service = ParticipantStateServiceGraphDB()

        result = participant_state_service.update_participant_state(id_node, participant_state_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
