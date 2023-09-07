import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut
from measure_name.measure_name_model import *
from models.not_found_model import *

from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from graph_api_service import GraphApiService


class TestMeasureNameServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_name_without_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Measure Name'],
                                      'properties': [{'key': 'name', 'value': 'Familiarity'},
                                                     {'key': 'type', 'value': 'Additional emotions measure'}],
                                      "errors": None, 'links': None}
        measure_name = BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=id_node)
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_name(id_node, dataset_name)

        self.assertEqual(result, measure_name)
        get_node_mock.assert_called_once_with(id_node,dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_name_without_participant_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_name(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_name_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_name(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measure_names(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Measure Name'],
                                                  'properties': [{'key': 'name', 'value': 'Familiarity'},
                                                                 {'key': 'type',
                                                                  'value': 'Additional emotions measure'}]},
                                                 {'id': 2, 'labels': ['Measure Name'],
                                                  'properties': [{'key': 'name', 'value': 'Familiarity'},
                                                                 {'key': 'type',
                                                                  'value': 'Additional emotions measure'}]}],
                                       'errors': None}
        measure_name_one = BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=1)
        measure_name_two = BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=2)
        measure_names = MeasureNamesOut(measure_names=[measure_name_one, measure_name_two])
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_names(dataset_name)

        self.assertEqual(result, measure_names)
        get_nodes_mock.assert_called_once_with("`Measure Name`", dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measure_names_empty(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        measure_names = MeasureNamesOut(measure_names=[])
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_names(dataset_name)

        self.assertEqual(result, measure_names)
        get_nodes_mock.assert_called_once_with("`Measure Name`", dataset_name)
