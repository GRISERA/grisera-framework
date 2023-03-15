import unittest
import unittest.mock as mock

from grisera_api.activity_execution.activity_execution_model import BasicActivityExecutionOut
from grisera_api.arrangement.arrangement_model import *
from grisera_api.arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from grisera_api.graph_api_service import GraphApiService
from grisera_api.models.not_found_model import *


class TestArrangementServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_arrangement_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Arrangement'],
                                      'properties': [{'key': 'arrangement_type', 'value': 'test'},
                                                     {'key': 'arrangement_distance', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": 19, "end_node": id_node,
             "name": "hasArrangement", "id": 0,
             "properties": None}]}
        arrangement = ArrangementOut(arrangement_type="test", arrangement_distance="test", id=id_node,
                                     activity_executions=[BasicActivityExecutionOut(**{id: 19})])
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.get_arrangement(id_node)

        self.assertEqual(result, arrangement)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_arrangement_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.get_arrangement(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_arrangement_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.get_arrangement(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_arrangements(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Arrangement'],
                                                  'properties': [{'key': 'arrangement_type', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['Arrangement'],
                                                  'properties': [{'key': 'arrangement_type', 'value': 'test2'}]}],
                                       'errors': None}
        arrangement_one = BasicArrangementOut(arrangement_type="test",  id=1)
        arrangement_two = BasicArrangementOut(arrangement_type="test2",  id=2)
        arrangements = ArrangementsOut(arrangements=[arrangement_one, arrangement_two])
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.get_arrangements()

        self.assertEqual(result, arrangements)
        get_nodes_mock.assert_called_once_with("Arrangement")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_arrangements_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [], 'errors': None}
        arrangements = ArrangementsOut(arrangements=[])
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.get_arrangements()

        self.assertEqual(result, arrangements)
        get_nodes_mock.assert_called_once_with("Arrangement")
