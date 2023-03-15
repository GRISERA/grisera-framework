import asyncio
import unittest
import unittest.mock as mock

from grisera_api.arrangement.arrangement_model import BasicArrangementOut
from grisera_api.arrangement.arrangement_router import *
from grisera_api.arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB


class TestArrangementRouterGet(unittest.TestCase):

    @mock.patch.object(ArrangementServiceGraphDB, 'get_arrangement')
    def test_get_arrangement_without_error(self, get_arrangement_mock):
        arrangement_id = 1
        get_arrangement_mock.return_value = ArrangementOut(arrangement_type='personal two persons',
                                                           arrangement_distance='intimate zone', id=arrangement_id)
        response = Response()
        arrangement_router = ArrangementRouter()

        result = asyncio.run(arrangement_router.get_arrangement(arrangement_id, response))

        self.assertEqual(result, ArrangementOut(arrangement_type='personal two persons',
                                                arrangement_distance='intimate zone', id=arrangement_id,
                                                links=get_links(router)))
        get_arrangement_mock.assert_called_once_with(arrangement_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ArrangementServiceGraphDB, 'get_arrangement')
    def test_get_arrangement_with_error(self, get_arrangement_mock):
        get_arrangement_mock.return_value = ArrangementOut(arrangement_type='personal two persons',
                                                           arrangement_distance='intimate zone',
                                                           errors={'errors': ['test']})
        response = Response()
        arrangement_id = 1
        arrangement_router = ArrangementRouter()

        result = asyncio.run(arrangement_router.get_arrangement(arrangement_id, response))

        self.assertEqual(result, ArrangementOut(arrangement_type='personal two persons',
                                                arrangement_distance='intimate zone', errors={'errors': ['test']},
                                                links=get_links(router)))
        get_arrangement_mock.assert_called_once_with(arrangement_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ArrangementServiceGraphDB, 'get_arrangements')
    def test_get_arrangement_nodes_without_error(self, get_arrangements_mock):
        get_arrangements_mock.return_value = ArrangementsOut(arrangements=[
            BasicArrangementOut(arrangement_type='personal two persons', arrangement_distance='intimate zone', id=1),
            BasicArrangementOut(arrangement_type='personal two persons', arrangement_distance='casual personal zone',
                                id=2)])
        response = Response()
        arrangement_router = ArrangementRouter()

        result = asyncio.run(arrangement_router.get_arrangements(response))

        self.assertEqual(result, ArrangementsOut(arrangements=[
            BasicArrangementOut(arrangement_type='personal two persons', arrangement_distance='intimate zone', id=1),
            BasicArrangementOut(arrangement_type='personal two persons', arrangement_distance='casual personal zone',
                                id=2)],
            links=get_links(router)))
        get_arrangements_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
