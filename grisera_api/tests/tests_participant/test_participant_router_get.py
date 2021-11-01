import asyncio
import unittest
import unittest.mock as mock
from participant.participant_router import *
from participant.participant_model import BasicParticipantOut


class TestParticipantRouterGet(unittest.TestCase):

    @mock.patch.object(ParticipantService, 'get_participant')
    def test_get_participant_without_error(self, get_participant_mock):
        participant_id = 1
        get_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', id=participant_id)
        response = Response()
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.get_participant(participant_id, response))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', id=participant_id,
                                                        links=get_links(router)))
        get_participant_mock.assert_called_once_with(participant_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantService, 'get_participant')
    def test_get_participant_with_error(self, get_participant_mock):
        get_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', errors={'errors': ['test']})
        response = Response()
        participant_id = 1
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.get_participant(participant_id, response))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', errors={'errors': ['test']},
                                                        links=get_links(router)))
        get_participant_mock.assert_called_once_with(participant_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ParticipantService, 'get_participants')
    def test_get_participants_without_error(self, get_participants_mock):
        get_participants_mock.return_value = ParticipantsOut(participants=[
            BasicParticipantOut(name="Test Test", sex='male', id=1),
            BasicParticipantOut(name="Test", sex='female', id=2)])
        response = Response()
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.get_participants(response))

        self.assertEqual(result, ParticipantsOut(participants=[
            BasicParticipantOut(name="Test Test", sex='male', id=1),
            BasicParticipantOut(name="Test", sex='female', id=2)],
            links=get_links(router)))
        get_participants_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
