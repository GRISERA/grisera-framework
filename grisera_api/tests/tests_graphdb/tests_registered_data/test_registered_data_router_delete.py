import asyncio
import unittest
import unittest.mock as mock
from grisera_api.registered_data.registered_data_router import *
from grisera_api.property.property_model import PropertyIn
from grisera_api.registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredDataRouterDelete(unittest.TestCase):

    @mock.patch.object(RegisteredDataServiceGraphDB, 'delete_registered_data')
    def test_delete_registered_data_without_error(self, delete_registered_data_mock):
        registered_data_id = 1
        delete_registered_data_mock.return_value = RegisteredDataOut(source='url', id=registered_data_id,
                                                                     additional_properties=[PropertyIn(key="test", value="test")])
        response = Response()
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.delete_registered_data(registered_data_id, response))

        self.assertEqual(result, RegisteredDataOut(source='url', id=registered_data_id,
                                                   additional_properties=[PropertyIn(key="test", value="test")],
                                                   links=get_links(router)))
        delete_registered_data_mock.assert_called_once_with(registered_data_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredDataServiceGraphDB, 'delete_registered_data')
    def test_delete_registered_data_with_error(self, delete_registered_data_mock):
        delete_registered_data_mock.return_value = RegisteredDataOut(source='url', errors={'errors': ['test']})
        response = Response()
        registered_data_id = 1
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.delete_registered_data(registered_data_id, response))

        self.assertEqual(result, RegisteredDataOut(source='url', errors={'errors': ['test']}, links=get_links(router)))
        delete_registered_data_mock.assert_called_once_with(registered_data_id)
        self.assertEqual(response.status_code, 404)
