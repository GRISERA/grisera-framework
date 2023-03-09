import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from registered_data.registered_data_model import *
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredDataServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_registered_data_without_error(self, create_properties_mock, create_node_mock):
        database_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'source', 'value': 'url'}],
                                               "errors": None, 'links': None}
        additional_properties = [PropertyIn(key='testkey', value='testvalue')]
        registered_data = RegisteredDataIn(source='url', additional_properties=additional_properties)
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.save_registered_data(registered_data, database_name)

        self.assertEqual(result, RegisteredDataOut(source='url', id=id_node, additional_properties=additional_properties))
        create_node_mock.assert_called_once_with('`Registered Data`', database_name)
        create_properties_mock.assert_called_once_with(id_node, registered_data, database_name)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_registered_data_with_node_error(self, create_node_mock):
        database_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        registered_data = RegisteredDataIn(source='url')
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.save_registered_data(registered_data, database_name)

        self.assertEqual(result, RegisteredDataOut(source='url', errors=['error']))
        create_node_mock.assert_called_once_with('`Registered Data`', database_name)

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_registered_data_with_properties_error(self, create_properties_mock, create_node_mock):
        database_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        registered_data = RegisteredDataIn(source='url')
        registered_data_service = RegisteredDataServiceGraphDB()

        result = registered_data_service.save_registered_data(registered_data, database_name)

        self.assertEqual(result, RegisteredDataOut(source='url', errors=['error']))
        create_node_mock.assert_called_once_with('`Registered Data`', database_name)
        create_properties_mock.assert_called_once_with(id_node, registered_data, database_name)
