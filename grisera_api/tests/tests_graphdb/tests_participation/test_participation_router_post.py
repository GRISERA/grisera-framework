import asyncio
import unittest
import unittest.mock as mock

from participation.participation_router import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB


class TestParticipationRouterPost(unittest.TestCase):

    @mock.patch.object(ParticipationServiceGraphDB, 'save_participation')
    def test_create_participation_without_error(self, save_participation_mock):
        database_name = "neo4j"
        save_participation_mock.return_value = ParticipationOut(activity_execution_id=2, participant_state_id=3, id=1)
        response = Response()
        participation = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participation(participation, response, database_name))

        self.assertEqual(result, ParticipationOut(activity_execution_id=2, participant_state_id=3, id=1, links=get_links(router)))
        save_participation_mock.assert_called_once_with(participation, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationServiceGraphDB, 'save_participation')
    def test_create_participation_with_error(self, save_participation_mock):
        database_name = "neo4j"
        save_participation_mock.return_value = ParticipationOut(activity_execution_id=2, participant_state_id=3,
                                                                errors={'errors': ['test']})
        response = Response()
        participation = ParticipationIn(activity_execution_id=2, participant_state_id=3)
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participation(participation, response, database_name))

        self.assertEqual(result, ParticipationOut(activity_execution_id=2, participant_state_id=3,
                                                  errors={'errors': ['test']}, links=get_links(router)))
        save_participation_mock.assert_called_once_with(participation, database_name)
        self.assertEqual(response.status_code, 422)
