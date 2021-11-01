import asyncio
import unittest
import unittest.mock as mock
from participant.participant_router import *


class TestParticipantRouterPut(unittest.TestCase):

    @mock.patch.object(ParticipantService, 'update_participant')
    def test_update_participant_without_error(self, update_participant_mock):
        participant_id = 1
        update_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', id=participant_id)
        response = Response()
        participant = ParticipantIn(name="Test Test", sex='male')
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.update_participant(participant_id, participant, response))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', id=participant_id,
                                                links=get_links(router)))
        update_participant_mock.assert_called_once_with(participant_id, participant)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantService, 'update_participant')
    def test_update_participant_with_error(self, update_participant_mock):
        participant_id = 1
        update_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', errors={'errors': ['test']})
        response = Response()
        participant = ParticipantIn(name="Test Test", sex='male')
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.update_participant(participant_id, participant, response))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', errors={'errors': ['test']},
                                                links=get_links(router)))
        update_participant_mock.assert_called_once_with(participant_id, participant)
        self.assertEqual(response.status_code, 404)
