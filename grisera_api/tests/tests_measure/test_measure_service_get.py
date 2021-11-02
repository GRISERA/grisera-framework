import unittest
import unittest.mock as mock

from measure.measure_model import *
from models.not_found_model import *

from measure.measure_service import MeasureService
from graph_api_service import GraphApiService


class TestMeasureServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_measure_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Measure'],
                                      'properties': [{'key': 'data_type', 'value': 'Test'},
                                                                          {'key': 'range', 'value': 'Unknown'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        measure = MeasureOut(data_type="Test", range="Unknown", id=id_node,
                                                relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                               relation_id=0)],
                                                reversed_relations=[RelationInformation(second_node_id=15,
                                                                                        name="testReversedRelation",
                                                                                        relation_id=0)])
        measure_service = MeasureService()

        result = measure_service.get_measure(id_node)

        self.assertEqual(result, measure)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        measure_service = MeasureService()

        result = measure_service.get_measure(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_measure_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        measure_service = MeasureService()

        result = measure_service.get_measure(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measures(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Measure'],
                                                  'properties': [{'key': 'data_type', 'value': 'Test'},
                                                                          {'key': 'range', 'value': 'Unknown'}]},
                                                 {'id': 2, 'labels': ['Measure'],
                                                  'properties': [{'key': 'data_type', 'value': 'Test'},
                                                                          {'key': 'range', 'value': 'Unknown'}]}]}
        measure_one = BasicMeasureOut(id=1, data_type="Test", range="Unknown")
        measure_two = BasicMeasureOut(id=2, data_type="Test", range="Unknown")
        measures = MeasuresOut(measures=[measure_one, measure_two])
        measures_service = MeasureService()

        result = measures_service.get_measures()

        self.assertEqual(result, measures)
        get_nodes_mock.assert_called_once_with("`Measure`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measures_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        measures = MeasuresOut(measure=[])
        measures_service = MeasureService()

        result = measures_service.get_measures()

        self.assertEqual(result, measures)
        get_nodes_mock.assert_called_once_with("`Measure`")
