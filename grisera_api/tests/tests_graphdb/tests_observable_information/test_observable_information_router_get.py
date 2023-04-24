import asyncio
import unittest
import unittest.mock as mock

from observable_information.observable_information_model import *
from observable_information.observable_information_router import *
from observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB


class TestObservableInformationRouterGet(unittest.TestCase):

    @mock.patch.object(ObservableInformationServiceGraphDB, 'get_observable_information')
    def test_get_observable_information_without_error(self, get_observable_information_mock):
        observable_information_id = 1
        get_observable_information_mock.return_value = ObservableInformationOut(id=observable_information_id)
        response = Response()
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.get_observable_information(observable_information_id,
                                                                                      response))

        self.assertEqual(result, ObservableInformationOut(id=observable_information_id, links=get_links(router)))
        get_observable_information_mock.assert_called_once_with(observable_information_id, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ObservableInformationServiceGraphDB, 'get_observable_information')
    def test_get_observable_information_with_error(self, get_observable_information_mock):
        get_observable_information_mock.return_value = ObservableInformationOut(errors={'errors': ['test']})
        response = Response()
        observable_information_id = 1
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.get_observable_information(observable_information_id,
                                                                                      response))

        self.assertEqual(result, ObservableInformationOut(errors={'errors': ['test']},
                                                          links=get_links(router)))
        get_observable_information_mock.assert_called_once_with(observable_information_id, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ObservableInformationServiceGraphDB, 'get_observable_informations')
    def test_get_observable_informations_without_error(self, get_observable_informations_mock):
        get_observable_informations_mock.return_value = ObservableInformationsOut(observable_informations=[
            BasicObservableInformationOut(id=1),
            BasicObservableInformationOut(id=2)])
        response = Response()
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.get_observable_informations(response))

        self.assertEqual(result, ObservableInformationsOut(observable_informations=[
            BasicObservableInformationOut(id=1),
            BasicObservableInformationOut(id=2)],
            links=get_links(router)))
        get_observable_informations_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
