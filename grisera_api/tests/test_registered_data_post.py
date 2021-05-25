from registered_data.registered_data_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_registered_data(*args, **kwargs):
    return RegisteredDataOut(source="http://localhost", id=1)


class TestRegisteredDataPost(unittest.TestCase):

    @mock.patch.object(RegisteredDataService, 'save_registered_data')
    def test_registered_data_post_without_error(self, mock_service):
        mock_service.side_effect = return_registered_data
        response = Response()
        registered_data = RegisteredDataIn(source="http://localhost")
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.create_registered_data(registered_data, response))

        self.assertEqual(result, RegisteredDataOut(source="http://localhost", id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RegisteredDataService, 'save_registered_data')
    def test_registered_data_post_with_error(self, mock_service):
        mock_service.return_value = RegisteredDataOut(source="http://localhost", errors={'errors': ['test']})
        response = Response()
        registered_data = RegisteredDataIn(source="http://localhost")
        registered_data_router = RegisteredDataRouter()

        result = asyncio.run(registered_data_router.create_registered_data(registered_data, response))

        self.assertEqual(response.status_code, 422)
