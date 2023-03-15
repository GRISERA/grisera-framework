import asyncio
import unittest
import unittest.mock as mock

from participation.participation_model import *
from participation.participation_router import *
from participation.participation_service_graphdb import ParticipationServiceGraphDB


class TestParticipationRouterGet(unittest.TestCase):

    @mock.patch.object(ParticipationServiceGraphDB, 'get_participation')
    def test_get_participation_without_error(self, get_participation_mock):
        participation_id = 1
        get_participation_mock.return_value = ParticipationOut(id=participation_id)
        response = Response()
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.get_participation(participation_id, response))

        self.assertEqual(result, ParticipationOut(id=participation_id, links=get_links(router)))
        get_participation_mock.assert_called_once_with(participation_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationServiceGraphDB, 'get_participation')
    def test_get_participation_with_error(self, get_participation_mock):
        get_participation_mock.return_value = ParticipationOut(errors={'errors': ['test']})
        response = Response()
        participation_id = 1
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.get_participation(participation_id, response))

        self.assertEqual(result, ParticipationOut(errors={'errors': ['test']},
                                                  links=get_links(router)))
        get_participation_mock.assert_called_once_with(participation_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ParticipationServiceGraphDB, 'get_participations')
    def test_get_participations_without_error(self, get_participations_mock):
        get_participations_mock.return_value = ParticipationsOut(participations=[
            BasicParticipationOut(id=1),
            BasicParticipationOut(id=2)])
        response = Response()
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.get_participations(response))

        self.assertEqual(result, ParticipationsOut(participations=[
            BasicParticipationOut(id=1),
            BasicParticipationOut(id=2)],
            links=get_links(router)))
        get_participations_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
