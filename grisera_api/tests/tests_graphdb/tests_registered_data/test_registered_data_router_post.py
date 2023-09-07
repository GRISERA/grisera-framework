import asyncio
import unittest
import unittest.mock as mock

from registered_data.registered_data_router import *
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredDataRouterPost(unittest.TestCase):

    @mock.patch.object(RegisteredDataServiceGraphDB, 'save_registered_data')
    def test_create_registered_data_without_error(self, save_registered_data_mock):
        dataset_name = "neo4j"
        save_registered_data_mock.return_value = RegisteredDataOut(source='url', id=1)
        response = Response()
        registered_data = RegisteredDataIn(source='url')
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.create_registered_data(registered_data, response, dataset_name))

        self.assertEqual(result, RegisteredDataOut(source='url', id=1, links=get_links(router)))
        save_registered_data_mock.assert_called_once_with(registered_data, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredDataServiceGraphDB, 'save_registered_data')
    def test_create_registered_data_with_error(self, save_registered_data_mock):
        dataset_name = "neo4j"
        save_registered_data_mock.return_value = RegisteredDataOut(source='url', errors={'errors': ['test']})
        response = Response()
        registered_data = RegisteredDataIn(source='url')
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.create_registered_data(registered_data, response, dataset_name))

        self.assertEqual(result, RegisteredDataOut(source='url', errors={'errors': ['test']}, links=get_links(router)))
        save_registered_data_mock.assert_called_once_with(registered_data, dataset_name)
        self.assertEqual(response.status_code, 422)
