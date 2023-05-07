import asyncio
import unittest
import unittest.mock as mock
from registered_data.registered_data_router import *
from property.property_model import PropertyIn
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredDataRouterPut(unittest.TestCase):

    @mock.patch.object(RegisteredDataServiceGraphDB, 'update_registered_data')
    def test_update_registered_data_without_error(self, update_registered_data_mock):
        dataset_name = "neo4j"
        registered_data_id = 1
        additional_properties = [PropertyIn(key="test", value="test")]
        update_registered_data_mock.return_value = RegisteredDataOut(source='url',
                                                                     additional_properties=additional_properties,
                                                                     id=registered_data_id)
        response = Response()
        registered_data = RegisteredDataIn(source='url', additional_properties=additional_properties)
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.update_registered_data(registered_data_id, registered_data, response, dataset_name))

        self.assertEqual(result, RegisteredDataOut(source='url', additional_properties=additional_properties,
                                                   id=registered_data_id, links=get_links(router)))
        update_registered_data_mock.assert_called_once_with(registered_data_id, registered_data, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredDataServiceGraphDB, 'update_registered_data')
    def test_update_registered_data_with_error(self, update_registered_data_mock):
        dataset_name = "neo4j"
        registered_data_id = 1
        update_registered_data_mock.return_value = RegisteredDataOut(source='url', errors={'errors': ['test']})
        response = Response()
        registered_data = RegisteredDataIn(source='url')
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.update_registered_data(registered_data_id, registered_data, response, dataset_name))

        self.assertEqual(result, RegisteredDataOut(source='url', errors={'errors': ['test']}, links=get_links(router)))
        update_registered_data_mock.assert_called_once_with(registered_data_id, registered_data, dataset_name)
        self.assertEqual(response.status_code, 404)
