import unittest
import unittest.mock as mock

from registered_channel.registered_channel_model import BasicRegisteredChannelOut
from registered_data.registered_data_model import *
from models.not_found_model import *

from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB
from graph_api_service import GraphApiService


class TestRegisteredDataServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_registered_data_without_error(self, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Data'],
                                                                      'properties': [{'key': 'source', 'value': 'test'},
                                                                                     {'key': 'test', 'value': 'test'}],
                                                                      "errors": None, 'links': None}
        additional_properties = [PropertyIn(key="test", value="test")]
        registered_data = BasicRegisteredDataOut(source="test", additional_properties=additional_properties, id=id_node)
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.delete_registered_data(id_node)

        self.assertEqual(result, registered_data)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

        # @mock.patch.object(GraphApiService, 'delete_node')
        # @mock.patch.object(GraphApiService, 'get_node')
        # @mock.patch.object(GraphApiService, 'get_node_relationships')
        # def test_delete_registered_data_without_error(self, get_node_relationships_mock, get_node_mock,
        #                                               delete_node_mock):
        #     id_node = 1
        #     delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Data'],
        #                                                                   'properties': [
        #                                                                       {'key': 'source', 'value': 'test'},
        #                                                                       {'key': 'test', 'value': 'test'}],
        #                                                                   "errors": None, 'links': None}
        #     get_node_relationships_mock.return_value = {"relationships": [
        #         {"start_node": 19, "end_node": id_node,
        #          "name": "hasRegisteredData", "id": 0,
        #          "properties": None}]}
        #     additional_properties = [PropertyIn(key="test", value="test")]
        #     registered_data = RegisteredDataOut(source="test", additional_properties=additional_properties, id=id_node,
        #                                         registered_channels=[BasicRegisteredChannelOut(**{id: 19})])
        #     registered_data_service = RegisteredDataServiceGraphDB()
        #
        #     result = registered_data_service.delete_registered_data(id_node)
        #
        #     self.assertEqual(result, registered_data)
        #     get_node_mock.assert_called_once_with(id_node)
        #     delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_registered_data_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.delete_registered_data(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_registered_data_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.delete_registered_data(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
