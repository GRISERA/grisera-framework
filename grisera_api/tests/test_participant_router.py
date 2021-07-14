import asyncio
import unittest
import unittest.mock as mock

from participant.participant_router import *


class TestParticipantRouter(unittest.TestCase):

    @mock.patch.object(ParticipantService, 'save_participant')
    def test_create_participant_without_error(self, save_participant_mock):
        save_participant_mock.return_value = ParticipantOut(sex='male', identifier=5, id=1)
        response = Response()
        participant = ParticipantIn(sex='male', identifier=5)
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.create_participant(participant, response))

        self.assertEqual(result, ParticipantOut(sex='male', identifier=5, id=1, links=get_links(router)))
        save_participant_mock.assert_called_once_with(participant)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantService, 'save_participant')
    def test_create_participant_with_error(self, save_participant_mock):
        save_participant_mock.return_value = ParticipantOut(sex='male', identifier=5, id=1, errors={'errors': ['test']})
        response = Response()
        participant = ParticipantIn(sex='male', identifier=5)
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.create_participant(participant, response))

        self.assertEqual(result, ParticipantOut(sex='male', identifier=5, id=1,
                                                errors={'errors': ['test']}, links=get_links(router)))
        save_participant_mock.assert_called_once_with(participant)
        self.assertEqual(response.status_code, 422)
