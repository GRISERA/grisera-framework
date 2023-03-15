import unittest
import unittest.mock as mock

from grisera_api.appearance.appearance_model import *
from grisera_api.models.not_found_model import *

from grisera_api.appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from grisera_api.graph_api_service import GraphApiService
from grisera_api.participant_state.participant_state_model import BasicParticipantStateOut


class TestAppearanceServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_appearance_occlusion_without_error(self, get_node_relationships_mock, get_node_mock,
                                                       create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Appearance'],
                                      'properties': [{'key': 'glasses', 'value': True},
                                                     {'key': 'beard', 'value': "Heavy"},
                                                     {'key': 'moustache', 'value': "None"}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasAppearance", "id": 0,
             "properties": None}]}
        appearance_in = AppearanceOcclusionIn(glasses=True, beard="Heavy", moustache="None")
        appearance_out = AppearanceOcclusionOut(id=id_node, glasses=True, beard="Heavy", moustache="Heavy",
                                            participant_states=[
                                                BasicParticipantStateOut(**{id: 19})])
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_occlusion(id_node, appearance_in)

        self.assertEqual(result, appearance_out)
        get_node_mock.assert_called_once_with(id_node)
        create_properties_mock.assert_called_once_with(id_node, appearance_in)

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_appearance_somatotype_without_error(self, get_node_relationships_mock, get_node_mock,
                                                        create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Appearance'],
                                      'properties': [{'key': 'ectomorph', 'value': 1.5},
                                                     {'key': 'endomorph', 'value': 1.5},
                                                     {'key': 'mesomorph', 'value': 1.5}],
                                      'errors': None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        appearance_in = AppearanceSomatotypeIn(ectomorph=1.5, endomorph=1.5, mesomorph=1.5)
        appearance_out = AppearanceSomatotypeOut(id=id_node, ectomorph=1.5, endomorph=1.5, mesomorph=1.5,
                                                 relations=[
                                                     RelationInformation(second_node_id=19, name="testRelation",
                                                                         relation_id=0)],
                                                 reversed_relations=[
                                                     RelationInformation(second_node_id=15, name="testReversedRelation",
                                                                         relation_id=0)]
                                                 )
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_somatotype(id_node, appearance_in)

        self.assertEqual(result, appearance_out)
        get_node_mock.assert_called_once_with(id_node)
        create_properties_mock.assert_called_once_with(id_node, appearance_in)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_appearance_occlusion_without_appearance_label(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        appearance_in = AppearanceOcclusionIn(glasses=True, beard="Heavy", moustache="None")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_occlusion(id_node, appearance_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_appearance_somatotype_without_appearance_label(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        appearance_in = AppearanceSomatotypeIn(ectomorph=1.5, endomorph=1.5, mesomorph=1.5)
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_somatotype(id_node, appearance_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_appearance_occlusion_with_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        appearance_in = AppearanceOcclusionIn(glasses=True, beard="Heavy", moustache="None")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_occlusion(id_node, appearance_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_appearance_somatotype_with_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        appearance_in = AppearanceSomatotypeIn(ectomorph=1.5, endomorph=1.5, mesomorph=1.5)
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_somatotype(id_node, appearance_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    def test_update_appearance_somatotype_with_wrong_range(self):
        id_node = 1
        appearance_in = AppearanceSomatotypeIn(ectomorph=0.5, endomorph=1.5, mesomorph=1.5)
        appearance_out = AppearanceSomatotypeOut(ectomorph=0.5, endomorph=1.5, mesomorph=1.5,
                                                 errors="Scale range not between 1 and 7")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.update_appearance_somatotype(id_node, appearance_in)

        self.assertEqual(result, appearance_out)
