import unittest
import unittest.mock as mock

from appearance.appearance_model import *
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from graph_api_service import GraphApiService


class TestAppearanceServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_appearance_occlusion_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'glasses', 'value': True},
                                                                             {'key': 'beard', 'value': "Heavy"},
                                                                             {'key': 'moustache', 'value': "Heavy"}],
                                               "errors": None, 'links': None}
        appearance = AppearanceOcclusionIn(glasses=True, beard="Heavy", moustache="Heavy")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.save_appearance_occlusion(appearance)

        self.assertEqual(result, AppearanceOcclusionOut(glasses=True, beard="Heavy", moustache="Heavy", id=id_node))
        create_node_mock.assert_called_once_with('Appearance')
        create_properties_mock.assert_called_once_with(id_node, appearance)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_appearance_occlusion_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        appearance = AppearanceOcclusionIn(glasses=False, beard="Heavy", moustache="Heavy")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.save_appearance_occlusion(appearance)

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", errors=['error']))
        create_node_mock.assert_called_once_with('Appearance')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_appearance_occlusion_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        appearance = AppearanceOcclusionIn(glasses=True, beard="Heavy", moustache="Heavy")
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.save_appearance_occlusion(appearance)

        self.assertEqual(result, AppearanceOcclusionOut(glasses=True, beard="Heavy", moustache="Heavy", errors=['error']))
        create_node_mock.assert_called_once_with('Appearance')
        create_properties_mock.assert_called_once_with(id_node, appearance)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_appearance_somatotype_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'ectomorph', 'value': 1.5},
                                                                             {'key': 'endomorph', 'value': 1.5},
                                                                             {'key': 'mesomorph', 'value': 1.5}],
                                               "errors": None, 'links': None}
        appearance = AppearanceSomatotypeIn(ectomorph=1.5, endomorph=1.5, mesomorph=1.5)
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.save_appearance_somatotype(appearance)

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=1.5, endomorph=1.5,
                                                        mesomorph=1.5, id=id_node))
        create_node_mock.assert_called_once_with('Appearance')
        create_properties_mock.assert_called_once_with(id_node, appearance)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_appearance_somatotype_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        appearance = AppearanceSomatotypeIn(ectomorph=1.5, endomorph=1.5, mesomorph=1.5)
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.save_appearance_somatotype(appearance)

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=1.5, endomorph=1.5,
                                                         mesomorph=1.5, errors=['error']))
        create_node_mock.assert_called_once_with('Appearance')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_appearance_somatotype_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        appearance = AppearanceSomatotypeIn(ectomorph=1.5, endomorph=1.5, mesomorph=1.5)
        appearance_service = AppearanceServiceGraphDB()

        result = appearance_service.save_appearance_somatotype(appearance)

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=1.5, endomorph=1.5,
                                                         mesomorph=1.5, errors=['error']))
        create_node_mock.assert_called_once_with('Appearance')
        create_properties_mock.assert_called_once_with(id_node, appearance)