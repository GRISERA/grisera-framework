import asyncio
import unittest
import unittest.mock as mock

from observable_information.observable_information_router import *
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB


class TestObservableInformationRouterDelete(unittest.TestCase):

    @mock.patch.object(ObservableInformationServiceGraphDB, 'delete_observable_information')
    def test_delete_observable_information_without_error(self, delete_observable_information_mock):
        observable_information_id = 1
        delete_observable_information_mock.return_value = ObservableInformationOut(id=observable_information_id)
        response = Response()
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.delete_observable_information(observable_information_id, response))

        self.assertEqual(result, ObservableInformationOut(id=observable_information_id, links=get_links(router)))
        delete_observable_information_mock.assert_called_once_with(observable_information_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ObservableInformationServiceGraphDB, 'delete_observable_information')
    def test_delete_observable_information_with_error(self, delete_observable_information_mock):
        delete_observable_information_mock.return_value = ObservableInformationOut(errors={'errors': ['test']})
        response = Response()
        observable_information_id = 1
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.delete_observable_information(observable_information_id, response))

        self.assertEqual(result, ObservableInformationOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_observable_information_mock.assert_called_once_with(observable_information_id)
        self.assertEqual(response.status_code, 404)