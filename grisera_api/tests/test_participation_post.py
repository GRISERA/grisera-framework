from participation.participation_router import *
from participation.participation_model import *
import unittest
import unittest.mock as mock
import asyncio


def return_participations(*args, **kwargs):
    participations_out = ParticipationsOut(participations=[ParticipationOut(activity_id=1, participant_state_id=1, id=2)])
    return participations_out


class TestParticipationsPost(unittest.TestCase):

    @mock.patch.object(ParticipationService, 'save_participations')
    def test_participations_post_without_error(self, mock_service):
        mock_service.side_effect = return_participations
        response = Response()
        participations = ParticipationsIn(activities=[1], participant_state_id=1)
        participation_router = ParticipationRouter()

        result = asyncio.run(participation_router.create_participations(participations, response))

        self.assertEqual(result, ParticipationsOut(participations=[ParticipationOut(activity_id=1, participant_state_id=1, id=2)],
                                               links=get_links(router)))
        self.assertEqual(response.status_code, 200)
