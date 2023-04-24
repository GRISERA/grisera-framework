import unittest
import unittest.mock as mock

from registered_data.registered_data_model import *
from models.not_found_model import *

from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB
from graph_api_service import GraphApiService


class TestRegisteredDataServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_registered_data_without_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Data'],
                                      'properties': [{'key': 'source', 'value': 'test'},
                                                     {'key': 'test', 'value': 'test'}],
                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='test', value="test")]
        registered_data = BasicRegisteredDataOut(id=id_node, source="test", additional_properties=additional_properties)
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.get_registered_data(id_node)

        self.assertEqual(result, registered_data)
        get_node_mock.assert_called_once_with(id_node)

    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_get_registered_data_without_error(self, get_node_relationships_mock, get_node_mock):
    #     id_node = 1
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Data'],
    #                                   'properties': [{'key': 'source', 'value': 'test'},
    #                                                  {'key': 'test', 'value': 'test'}],
    #                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": 19, "end_node": id_node,
    #          "name": "hasRegisteredData", "id": 0,
    #          "properties": None}]}
    #     additional_properties = [PropertyIn(key='test', value="test")]
    #     registered_data = RegisteredDataOut(source="test", additional_properties=additional_properties, id=id_node,
    #                                         registered_channels=[BasicRegisteredChannelOut(**{id: 19})])
    #     registered_data_service = RegisteredDataServiceGraphDB()
    #
    #     result = registered_data_service.get_registered_data(id_node)
    #
    #     self.assertEqual(result, registered_data)
    #     get_node_mock.assert_called_once_with(id_node)
    #     get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_registered_data_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.get_registered_data(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_registered_data_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.get_registered_data(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_registered_data_nodes(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['`Registered Data`'],
                                                  'properties': [{'key': 'source', 'value': 'test'}]},
                                                 {'id': 2, 'labels': ['`Registered Data`'],
                                                  'properties': [{'key': 'source', 'value': 'test2'}]}]}
        registered_data_one = BasicRegisteredDataOut(source="test", id=1, additional_properties=[])
        registered_data_two = BasicRegisteredDataOut(source="test2", id=2, additional_properties=[])
        registered_data_nodes = RegisteredDataNodesOut(registered_data_nodes=[registered_data_one, registered_data_two])
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.get_registered_data_nodes()

        self.assertEqual(result, registered_data_nodes)
        get_nodes_mock.assert_called_once_with("Registered Data")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_registered_data_nodes_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        registered_data_nodes = RegisteredDataNodesOut(registered_data_nodes=[])
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.get_registered_data_nodes()

        self.assertEqual(result, registered_data_nodes)
        get_nodes_mock.assert_called_once_with("Registered Data")
