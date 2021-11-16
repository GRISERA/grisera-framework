import asyncio
import unittest
import unittest.mock as mock

from participation.participation_router import *


class TestParticipationRouterDelete(unittest.TestCase):

    @mock.patch.object(ParticipationService, 'delete_participation')
    def test_delete_participation_without_error(self, delete_participation_mock):
        participation_id = 1
        delete_participation_mock.return_value = ParticipationOut(id=participation_id)
        response = Response()
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.delete_participation(participation_id, response))

        self.assertEqual(result, ParticipationOut(id=participation_id, links=get_links(router)))
        delete_participation_mock.assert_called_once_with(participation_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationService, 'delete_participation')
    def test_delete_participation_with_error(self, delete_participation_mock):
        delete_participation_mock.return_value = ParticipationOut(errors={'errors': ['test']})
        response = Response()
        participation_id = 1
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.delete_participation(participation_id, response))

        self.assertEqual(result, ParticipationOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_participation_mock.assert_called_once_with(participation_id)
        self.assertEqual(response.status_code, 404)