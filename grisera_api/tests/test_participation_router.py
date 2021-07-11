from participation.participation_router import *
import unittest
import unittest.mock as mock
import asyncio


class TestParticipationRouter(unittest.TestCase):

    @mock.patch.object(ParticipationService, 'save_participation')
    def test_create_participation_without_error(self, save_participation_mock):
        save_participation_mock.return_value = ParticipationOut(activity_id=2, participant_state_id=3, id=1)
        response = Response()
        participation = ParticipationIn(activity_id=2, participant_state_id=3)
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participation(participation, response))

        self.assertEqual(result, ParticipationOut(activity_id=2, participant_state_id=3, id=1, links=get_links(router)))
        save_participation_mock.assert_called_once_with(participation)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipationService, 'save_participation')
    def test_create_participation_with_error(self, save_participation_mock):
        save_participation_mock.return_value = ParticipationOut(activity_id=2, participant_state_id=3,
                                                                errors={'errors': ['test']})
        response = Response()
        participation = ParticipationIn(activity_id=2, participant_state_id=3)
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participation(participation, response))

        self.assertEqual(result, ParticipationOut(activity_id=2, participant_state_id=3,
                                                  errors={'errors': ['test']}, links=get_links(router)))
        save_participation_mock.assert_called_once_with(participation)
        self.assertEqual(response.status_code, 422)
