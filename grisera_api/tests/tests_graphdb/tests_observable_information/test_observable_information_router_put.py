import asyncio
import unittest
import unittest.mock as mock

from grisera_api.observable_information.observable_information_router import *
from grisera_api.observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB


class TestObservableInformationRouterPut(unittest.TestCase):

    @mock.patch.object(ObservableInformationServiceGraphDB, 'update_observable_information_relationships')
    def test_update_observable_information_relationships_without_error(
            self,
            update_observable_information_relationships_mock):
        id_node = 1
        update_observable_information_relationships_mock.return_value = ObservableInformationOut(id=id_node)
        response = Response()
        observable_information_in = ObservableInformationIn(modality_id=2, life_activity_id=3)
        observable_information_out = ObservableInformationOut(id=id_node, links=get_links(router))
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.
                             update_observable_information_relationships(id_node, observable_information_in, response))

        self.assertEqual(result, observable_information_out)
        update_observable_information_relationships_mock.assert_called_once_with(id_node, observable_information_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ObservableInformationServiceGraphDB, 'update_observable_information_relationships')
    def test_update_observable_information_relationships_with_error(self,
                                                                    update_observable_information_relationships_mock):
        id_node = 1
        update_observable_information_relationships_mock.return_value = ObservableInformationOut(id=id_node,
                                                                                                 errors="error")
        response = Response()
        observable_information_in = ObservableInformationIn(modality_id=2, life_activity_id=3)
        observable_information_out = ObservableInformationOut(id=id_node, errors="error", links=get_links(router))
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router.
                             update_observable_information_relationships(id_node, observable_information_in, response))

        self.assertEqual(result, observable_information_out)
        update_observable_information_relationships_mock.assert_called_once_with(id_node, observable_information_in)
        self.assertEqual(response.status_code, 404)
