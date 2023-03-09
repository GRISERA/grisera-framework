import asyncio
import unittest
import unittest.mock as mock

from observable_information.observable_information_router import *
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB


class TestObservableInformationRouterPost(unittest.TestCase):

    @mock.patch.object(ObservableInformationServiceGraphDB, 'save_observable_information')
    def test_create_observable_information_without_error(self, save_observable_information_mock):
        database_name = "neo4j"
        save_observable_information_mock.return_value = ObservableInformationOut(modality_id=2, life_activity_id=3, id=1)
        response = Response()
        observable_information = ObservableInformationIn(modality_id=2, life_activity_id=3)
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.create_observable_information(observable_information, response, database_name))

        self.assertEqual(result, ObservableInformationOut(modality_id=2, life_activity_id=3, id=1, links=get_links(router)))
        save_observable_information_mock.assert_called_once_with(observable_information, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ObservableInformationServiceGraphDB, 'save_observable_information')
    def test_create_observable_information_with_error(self, save_observable_information_mock):
        database_name = "neo4j"
        save_observable_information_mock.return_value = ObservableInformationOut(modality_id=2, life_activity_id=3,
                                                                errors={'errors': ['test']})
        response = Response()
        observable_information = ObservableInformationIn(modality_id=2, life_activity_id=3)
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.create_observable_information(observable_information, response, database_name))

        self.assertEqual(result, ObservableInformationOut(modality_id=2, life_activity_id=3,
                                                  errors={'errors': ['test']}, links=get_links(router)))
        save_observable_information_mock.assert_called_once_with(observable_information, database_name)
        self.assertEqual(response.status_code, 422)
