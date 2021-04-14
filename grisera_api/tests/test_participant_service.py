import json
import unittest
import unittest.mock as mock
from participant.participant_model import *
from participant.participant_service import ParticipantService
from requests import Response


class TestParticipantPostService(unittest.TestCase):

    @mock.patch('participant.participant_service.requests')
    def test_participant_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        participant = ParticipantIn()
        participant_service = ParticipantService()

        result = participant_service.save_participant(participant)

        self.assertEqual(result, ParticipantOut(id=1))

    @mock.patch('participant.participant_service.requests')
    def test_participant_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        participant = ParticipantIn()
        participant_service = ParticipantService()

        result = participant_service.save_participant(participant)

        self.assertEqual(result, ParticipantOut(errors={'error': 'test'}))
