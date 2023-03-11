import asyncio
import unittest
import unittest.mock as mock
from participant.participant_router import *
from participant.participant_service_graphdb import ParticipantServiceGraphDB


class TestParticipantRouterDelete(unittest.TestCase):

    @mock.patch.object(ParticipantServiceGraphDB, 'delete_participant')
    def test_delete_participant_without_error(self, delete_participant_mock):
        database_name = "neo4j"
        participant_id = 1
        delete_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', id=participant_id)
        response = Response()
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.delete_participant(participant_id, response, database_name))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', id=participant_id,
                                                links=get_links(router)))
        delete_participant_mock.assert_called_once_with(participant_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantServiceGraphDB, 'delete_participant')
    def test_delete_participant_with_error(self, delete_participant_mock):
        database_name = "neo4j"
        delete_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', errors={'errors': ['test']})
        response = Response()
        participant_id = 1
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.delete_participant(participant_id, response, database_name))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', errors={'errors': ['test']},
                                                links=get_links(router)))
        delete_participant_mock.assert_called_once_with(participant_id, database_name)
        self.assertEqual(response.status_code, 404)
