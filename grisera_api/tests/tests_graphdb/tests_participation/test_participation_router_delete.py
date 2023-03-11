import asyncio
import unittest
import unittest.mock as mock

from participation.participation_router import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB


class TestParticipationRouterDelete(unittest.TestCase):

    @mock.patch.object(ParticipationServiceGraphDB, 'delete_participation')
    def test_delete_participation_without_error(self, delete_participation_mock):
        database_name = "neo4j"
        participation_id = 1
        delete_participation_mock.return_value = ParticipationOut(id=participation_id)
        response = Response()
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.delete_participation(participation_id, response, database_name))

        self.assertEqual(result, ParticipationOut(id=participation_id, links=get_links(router)))
        delete_participation_mock.assert_called_once_with(participation_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationServiceGraphDB, 'delete_participation')
    def test_delete_participation_with_error(self, delete_participation_mock):
        database_name = "neo4j"
        delete_participation_mock.return_value = ParticipationOut(errors={'errors': ['test']})
        response = Response()
        participation_id = 1
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.delete_participation(participation_id, response, database_name))

        self.assertEqual(result, ParticipationOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_participation_mock.assert_called_once_with(participation_id, database_name)
        self.assertEqual(response.status_code, 404)