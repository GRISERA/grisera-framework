import unittest
import unittest.mock as mock

from appearance.appearance_model import *
from models.not_found_model import *

from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from graph_api_service import GraphApiService
from participant_state.participant_state_model import BasicParticipantStateOut


class TestAppearanceServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_appearance_occlusion_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Appearance'],
                                      'properties': [{'key': 'glasses', 'value': True},
                                                     {'key': 'beard', 'value': "Heavy"},
                                                     {'key': 'moustache', 'value': "Heavy"}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasAppearance", "id": 0,
             "properties": None}]}
        appearance = AppearanceOcclusionOut(id=id_node, glasses=True, beard="Heavy", moustache="Heavy",
                                            participant_states=[
                                                BasicParticipantStateOut(**{id: 19})])
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.get_appearance(id_node)

        self.assertEqual(result, appearance)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_appearance_somatotype_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Appearance'],
                                      'properties': [{'key': 'ectomorph', 'value': 1.5},
                                                     {'key': 'endomorph', 'value': 1.5},
                                                     {'key': 'mesomorph', 'value': 1.5}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasAppearance", "id": 0,
             "properties": None}]}
        appearance = AppearanceOcclusionOut(id=id_node, glasses=True, beard="Heavy", moustache="Heavy",
                                            participant_states=[
                                                BasicParticipantStateOut(**{id: 19})])
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.get_appearance(id_node)

        self.assertEqual(result, appearance)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_appearance_without_appearance_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.get_appearance(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_appearance_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.get_appearance(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_appearances(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Appearance'],
                                                  'properties': [{'key': 'glasses', 'value': True},
                                                                 {'key': 'beard', 'value': "Heavy"},
                                                                 {'key': 'moustache', 'value': "Heavy"}]},
                                                 {'id': 2, 'labels': ['Appearance'],
                                                  'properties': [{'key': 'ectomorph', 'value': 1.5},
                                                                 {'key': 'endomorph', 'value': 1.5},
                                                                 {'key': 'mesomorph', 'value': 1.5}]}]}
        appearance_occlusion = BasicAppearanceOcclusionOut(id=1, glasses=True, beard="Heavy", moustache="Heavy")
        appearance_somatotype = BasicAppearanceSomatotypeOut(id=2, ectomorph=1.5,
                                                             endomorph=1.5, mesomorph=1.5)
        appearances = AppearancesOut(appearances=[appearance_occlusion, appearance_somatotype])
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.get_appearances()

        self.assertEqual(result, appearances)
        get_nodes_mock.assert_called_once_with("Appearance")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_appearances_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        appearances = AppearancesOut(appearances=[])
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.get_appearances()

        self.assertEqual(result, appearances)
        get_nodes_mock.assert_called_once_with("Appearance")
