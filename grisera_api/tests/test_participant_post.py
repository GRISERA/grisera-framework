from participant.participant_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_participant(*args, **kwargs):
    participant_out = ParticipantOut(id=1)
    return participant_out


class TestParticipantPost(unittest.TestCase):

    @mock.patch.object(ParticipantService, 'save_participant')
    def test_participant_post_without_error(self, mock_service):
        mock_service.side_effect = return_participant
        response = Response()
        participant = ParticipantIn()
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.create_participant(participant, response))

        self.assertEqual(result, ParticipantOut(id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantService, 'save_participant')
    def test_participant_post_with_error(self, mock_service):
        mock_service.return_value = ParticipantOut(errors={'errors': ['test']})
        response = Response()
        participant = ParticipantIn()
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.create_participant(participant, response))

        self.assertEqual(response.status_code, 422)
