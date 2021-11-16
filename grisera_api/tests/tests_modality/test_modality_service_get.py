import unittest
import unittest.mock as mock

from modality.modality_model import *
from models.not_found_model import *

from modality.modality_service import ModalityService
from graph_api_service import GraphApiService


class TestModalityServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_modality_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Modality'],
                                      'properties': [{'key': 'modality', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        modality = ModalityOut(modality="test", id=id_node,
                               relations=[RelationInformation(second_node_id=19, name="testRelation", relation_id=0)],
                               reversed_relations=[RelationInformation(second_node_id=15, name="testReversedRelation", 
                                                                       relation_id=0)])
        modality_service = ModalityService()

        result = modality_service.get_modality(id_node)

        self.assertEqual(result, modality)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_modality_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        modality_service = ModalityService()

        result = modality_service.get_modality(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_modality_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        modality_service = ModalityService()

        result = modality_service.get_modality(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_modalities(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['`Modality`'],
                                                  'properties': [{'key': 'modality', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['`Modality`'],
                                                  'properties': [{'key': 'modality', 'value': 'test2'}]}]}
        modality_one = BasicModalityOut(modality="test", id=1)
        modality_two = BasicModalityOut(modality="test2", id=2)
        modalities = ModalitiesOut(modalities=[modality_one, modality_two])
        modality_service = ModalityService()

        result = modality_service.get_modalities()

        self.assertEqual(result, modalities)
        get_nodes_mock.assert_called_once_with("Modality")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_modalities_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        modalities = ModalitiesOut(modalities=[])
        modality_service = ModalityService()

        result = modality_service.get_modalities()

        self.assertEqual(result, modalities)
        get_nodes_mock.assert_called_once_with("Modality")
