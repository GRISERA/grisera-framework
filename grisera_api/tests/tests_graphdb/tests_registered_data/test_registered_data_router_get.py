import asyncio
import unittest
import unittest.mock as mock
from registered_data.registered_data_router import *
from registered_data.registered_data_model import BasicRegisteredDataOut
from property.property_model import PropertyIn
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredDataRouterGet(unittest.TestCase):

    @mock.patch.object(RegisteredDataServiceGraphDB, 'get_registered_data')
    def test_get_registered_data_without_error(self, get_registered_data_mock):
        registered_data_id = 1
        additional_properties = [PropertyIn(key="test", value="test")]
        get_registered_data_mock.return_value = RegisteredDataOut(source='url',
                                                                  additional_properties=additional_properties,
                                                                  id=registered_data_id)
        response = Response()
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.get_registered_data(registered_data_id, response))

        self.assertEqual(result, RegisteredDataOut(source='url', additional_properties=additional_properties,
                                                   id=registered_data_id, links=get_links(router)))
        get_registered_data_mock.assert_called_once_with(registered_data_id, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredDataServiceGraphDB, 'get_registered_data')
    def test_get_registered_data_with_error(self, get_registered_data_mock):
        additional_properties = [PropertyIn(key="test", value="test")]
        get_registered_data_mock.return_value = RegisteredDataOut(source='url',
                                                                  additional_properties=additional_properties,
                                                                  errors={'errors': ['test']})
        response = Response()
        registered_data_id = 1
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.get_registered_data(registered_data_id, response))

        self.assertEqual(result, RegisteredDataOut(source='url', additional_properties=additional_properties,
                                                   errors={'errors': ['test']},  links=get_links(router)))
        get_registered_data_mock.assert_called_once_with(registered_data_id, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(RegisteredDataServiceGraphDB, 'get_registered_data_nodes')
    def test_get_registered_data_nodes_without_error(self, get_registered_datas_mock):
        get_registered_datas_mock.return_value = RegisteredDataNodesOut(registered_data_nodes=[
            BasicRegisteredDataOut(source='url', id=1), BasicRegisteredDataOut(source='url2', id=2)])
        response = Response()
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.get_registered_data_nodes(response))

        self.assertEqual(result, RegisteredDataNodesOut(registered_data_nodes=[
            BasicRegisteredDataOut(source='url', id=1), BasicRegisteredDataOut(source='url2', id=2)],
            links=get_links(router)))
        get_registered_datas_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
