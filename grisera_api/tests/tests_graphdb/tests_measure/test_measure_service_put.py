import unittest
import unittest.mock as mock

from measure.measure_model import *
from measure_name.measure_name_model import BasicMeasureNameOut
from models.not_found_model import *

from measure.measure_service_graphdb import MeasureServiceGraphDB
from graph_api_service import GraphApiService
from time_series.time_series_model import BasicTimeSeriesOut


class TestMeasureServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    def test_update_measure_without_error(self, delete_node_properties_mock,
                                          get_node_mock, create_properties_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Measure'],
                                      'properties': [{'key': 'datatype', 'value': 'Test'},
                                                     {'key': 'range', 'value': 'Unknown'},
                                                     {'key': 'unit', 'value': 'cm'}],
                                      "errors": None, 'links': None}
        measure_in = MeasurePropertyIn(datatype="Test", range="Unknown", unit="cm", id=id_node)

        measure_out = BasicMeasureOut(datatype="Test", range="Unknown", unit="cm", id=id_node)
        calls = [mock.call(1,dataset_name)]
        measure_service = MeasureServiceGraphDB()

        result = measure_service.update_measure(id_node, measure_in, dataset_name)

        self.assertEqual(result, measure_out)
        get_node_mock.assert_has_calls(calls)

        create_properties_mock.assert_called_once_with(id_node, measure_in,dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_measure_without_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        measure_in = MeasurePropertyIn(datatype="Test", range="Unknown", unit="cm")
        measure_service = MeasureServiceGraphDB()

        result = measure_service.update_measure(id_node, measure_in, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_measure_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        measure_in = MeasurePropertyIn(datatype="Test", range="Unknown", unit="cm")
        measure_service = MeasureServiceGraphDB()

        result = measure_service.update_measure(id_node, measure_in, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
