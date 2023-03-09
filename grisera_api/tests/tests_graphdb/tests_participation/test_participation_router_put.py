import asyncio
import unittest
import unittest.mock as mock

from participation.participation_router import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB


class TestParticipationRouterPut(unittest.TestCase):

    @mock.patch.object(ParticipationServiceGraphDB, 'update_participation_relationships')
    def test_update_participation_relationships_without_error(self, update_participation_relationships_mock):
        database_name = "neo4j"
        id_node = 1
        update_participation_relationships_mock.return_value = ParticipationOut(id=id_node)
        response = Response()
        participation_in = ParticipationIn(activity_execution_id=2, arrangement_id=3)
        participation_out = ParticipationOut(id=id_node, links=get_links(router))
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.
                             update_participation_relationships(id_node, participation_in, response, database_name))

        self.assertEqual(result, participation_out)
        update_participation_relationships_mock.assert_called_once_with(id_node, participation_in, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationServiceGraphDB, 'update_participation_relationships')
    def test_update_participation_relationships_with_error(self, update_participation_relationships_mock):
        database_name = "neo4j"
        id_node = 1
        update_participation_relationships_mock.return_value = ParticipationOut(id=id_node, errors="error")
        response = Response()
        participation_in = ParticipationIn(activity_execution_id=2, arrangement_id=3)
        participation_out = ParticipationOut(id=id_node, errors="error", links=get_links(router))
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.
                             update_participation_relationships(id_node, participation_in, response, database_name))

        self.assertEqual(result, participation_out)
        update_participation_relationships_mock.assert_called_once_with(id_node, participation_in, database_name)
        self.assertEqual(response.status_code, 404)