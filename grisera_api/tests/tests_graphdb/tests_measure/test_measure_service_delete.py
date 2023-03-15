import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from measure.measure_model import *
from measure.measure_service_graphdb import MeasureServiceGraphDB
from measure_name.measure_name_model import BasicMeasureNameOut
from models.not_found_model import *
from time_series.time_series_model import BasicTimeSeriesOut


class TestMeasureServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_measure_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Measure'],
                                                                      'properties': [
                                                                          {'key': 'datatype', 'value': 'Test'},
                                                                          {'key': 'range', 'value': 'Unknown'},
                                                                          {'key': 'unit', 'value': 'cm'}],
                                                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasMeasure", "id": 0,
             "properties": None},
            {"start_node": id_node, "end_node": 15,
             "name": "hasMeasureName", "id": 0,
             "properties": None}]}
        measure = MeasureOut(datatype="Test", range="Unknown", unit="cm", id=id_node,
                             time_series=[BasicTimeSeriesOut(**{id: 15})], measure_name=BasicMeasureNameOut(**{id: 15}))
        measure_service = MeasureServiceGraphDB()

        result = measure_service.delete_measure(id_node)

        self.assertEqual(result, measure)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_measure_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        measure_service = MeasureServiceGraphDB()

        result = measure_service.delete_measure(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_measure_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        measure_service = MeasureServiceGraphDB()

        result = measure_service.delete_measure(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
