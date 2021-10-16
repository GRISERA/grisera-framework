import asyncio
import unittest
import unittest.mock as mock
from participant_state.participant_state_router import *


class TestParticipantStateRouterPut(unittest.TestCase):

    @mock.patch.object(ParticipantStateService, 'update_participant_state')
    def test_update_participant_state_without_error(self, update_participant_state_mock):
        participant_state_id = 1
        update_participant_state_mock.return_value = ParticipantStateRelationOut(age=5, id=participant_state_id)
        response = Response()
        participant_state = ParticipantStateIn(age=5)
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.update_participant_state(
            participant_state_id, participant_state, response))

        self.assertEqual(result, ParticipantStateRelationOut(age=5, id=participant_state_id, links=get_links(router)))
        update_participant_state_mock.assert_called_once_with(participant_state_id, participant_state)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateService, 'update_participant_state')
    def test_update_participant_state_with_error(self, update_participant_state_mock):
        participant_state_id = 1
        update_participant_state_mock.return_value = ParticipantStateRelationOut(age=5, errors={'errors': ['test']})
        response = Response()
        participant_state = ParticipantStateIn(age=5)
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.update_participant_state(
            participant_state_id, participant_state, response))

        self.assertEqual(result, ParticipantStateRelationOut(age=5, errors={'errors': ['test']},
                                                             links=get_links(router)))
        update_participant_state_mock.assert_called_once_with(participant_state_id, participant_state)
        self.assertEqual(response.status_code, 404)
