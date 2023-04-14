import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from measure.measure_model import *
from measure.measure_service_graphdb import MeasureServiceGraphDB
from models.not_found_model import *


class TestMeasureServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_measure_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Measure'],
                                                                      'properties': [
                                                                          {'key': 'datatype', 'value': 'Test'},
                                                                          {'key': 'range', 'value': 'Unknown'},
                                                                          {'key': 'unit', 'value': 'cm'}],
                                                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        measure = MeasureOut(datatype="Test", range="Unknown", unit="cm", id=id_node,
                             relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                            relation_id=0)],
                             reversed_relations=[RelationInformation(second_node_id=15,
                                                                     name="testReversedRelation",
                                                                     relation_id=0)])
        measure_service = MeasureServiceGraphDB()

        result = measure_service.delete_measure(id_node, dataset_name)

        self.assertEqual(result, measure)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
        delete_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_measure_without_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        measure_service = MeasureServiceGraphDB()

        result = measure_service.delete_measure(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_measure_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        measure_service = MeasureServiceGraphDB()

        result = measure_service.delete_measure(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
