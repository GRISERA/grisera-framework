import unittest
import unittest.mock as mock

from grisera_api.measure.measure_model import BasicMeasureOut
from grisera_api.measure_name.measure_name_model import *
from grisera_api.models.not_found_model import *

from grisera_api.measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from grisera_api.graph_api_service import GraphApiService


class TestMeasureNameServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_measure_name_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Measure Name'],
                                      'properties': [{'key': 'name', 'value': 'Familiarity'},
                                                     {'key': 'type', 'value': 'Additional emotions measure'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "hasMeasureName", "id": 0,
             "properties": None}]}
        measure_name = MeasureNameOut(name="Familiarity", type="Additional emotions measure", id=id_node,
                                      measures=[BasicMeasureOut(**{id: 19})])
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_name(id_node)

        self.assertEqual(result, measure_name)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_name_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_name(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_name_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_name(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measure_names(self, get_nodes_mock):
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

        result = measure_name_service.get_measure_names()

        self.assertEqual(result, measure_names)
        get_nodes_mock.assert_called_once_with("`Measure Name`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measure_names_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        measure_names = MeasureNamesOut(measure_names=[])
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.get_measure_names()

        self.assertEqual(result, measure_names)
        get_nodes_mock.assert_called_once_with("`Measure Name`")
