from participant_state.participant_state_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_participant_state(*args, **kwargs):
    participant_state_out = ParticipantStateOut(id=1)
    return participant_state_out


class TestParticipantStatePost(unittest.TestCase):

    @mock.patch.object(ParticipantStateService, 'save_participant_state')
    def test_participant_state_post_without_error(self, mock_service):
        mock_service.side_effect = return_participant_state
        response = Response()
        participant_state = ParticipantStateIn()
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.create_participant_state(participant_state, response))

        self.assertEqual(result, ParticipantStateOut(id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateService, 'save_participant_state')
    def test_participant_state_post_with_error(self, mock_service):
        mock_service.return_value = ParticipantStateOut(errors={'errors': ['test']})
        response = Response()
        participant_state = ParticipantStateIn()
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.create_participant_state(participant_state, response))

        self.assertEqual(response.status_code, 422)
