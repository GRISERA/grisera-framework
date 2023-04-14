import unittest
import unittest.mock as mock

from time_series.time_series_model import *
from models.not_found_model import *

from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from graph_api_service import GraphApiService


class TestTimeSeriesServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_time_series_without_error(self, get_node_relationships_mock, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Time Series'],
                                      'properties': [{'key': 'type', 'value': "Epoch"},
                                                     {'key': 'source', 'value': "cos"},
                                                     {'key': 'test', 'value': 'test2'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        additional_properties = [PropertyIn(key='test', value='test2')]
        time_series = TimeSeriesOut(id=1, type="Epoch", source="cos",additional_properties=additional_properties,
                                                relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                               relation_id=0)],
                                                reversed_relations=[RelationInformation(second_node_id=15,
                                                                                        name="testReversedRelation",
                                                                                        relation_id=0)])
        time_series_service = TimeSeriesServiceGraphDB()

        result = time_series_service.get_time_series(id_node, dataset_name)

        self.assertEqual(result, time_series)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
        get_node_relationships_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_time_series_without_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        time_series_service = TimeSeriesServiceGraphDB()

        result = time_series_service.get_time_series(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_time_series_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        time_series_service = TimeSeriesServiceGraphDB()

        result = time_series_service.get_time_series(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_time_series_nodes(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Time Series'],
                                                  'properties': [{'key': 'type', 'value': "Epoch"},
                                                     {'key': 'source', 'value': "cos"},
                                                                 {'key': 'test', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Time Series'],
                                                  'properties': [{'key': 'type', 'value': "Epoch"},
                                                     {'key': 'source', 'value': "cos"},
                                                                 {'key': 'test2', 'value': 'test3'}]}]}
        time_series_one = BasicTimeSeriesOut(id=1, type="Epoch", source="cos", additional_properties=[
            PropertyIn(key='test', value='test')])
        time_series_two = BasicTimeSeriesOut(id=2, type="Epoch", source="cos", additional_properties=[
            PropertyIn(key='test2', value='test3')])
        time_series_nodes = TimeSeriesNodesOut(time_series_nodes=[time_series_one, time_series_two])
        time_series_nodes_service = TimeSeriesServiceGraphDB()

        result = time_series_nodes_service.get_time_series_nodes(dataset_name)

        self.assertEqual(result, time_series_nodes)
        get_nodes_mock.assert_called_once_with("`Time Series`", dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_time_series_nodes_empty(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': []}
        time_series_nodes = TimeSeriesNodesOut(time_series=[])
        time_series_nodes_service = TimeSeriesServiceGraphDB()

        result = time_series_nodes_service.get_time_series_nodes(dataset_name)

        self.assertEqual(result, time_series_nodes)
        get_nodes_mock.assert_called_once_with("`Time Series`", dataset_name)
