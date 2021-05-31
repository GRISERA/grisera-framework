from participation.participation_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_participation(*args, **kwargs):
    participation_out = ParticipationOut(id=1)
    return participation_out


class TestParticipationPost(unittest.TestCase):

    @mock.patch.object(ParticipationService, 'save_participation')
    def test_participation_post_without_error(self, mock_service):
        mock_service.side_effect = return_participation
        response = Response()
        participation = ParticipationIn()
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participation(response))

        self.assertEqual(result, ParticipationOut(id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationService, 'save_participation')
    def test_participation_post_with_error(self, mock_service):
        mock_service.return_value = ParticipationOut(errors={'errors': ['test']})
        response = Response()
        participation = ParticipationIn()
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participation(response))

        self.assertEqual(response.status_code, 422)
