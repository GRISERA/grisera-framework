import json
import unittest
import unittest.mock as mock
from participant_state.participant_state_model import *
from participant_state.participant_state_service import ParticipantStateService
from requests import Response


class TestParticipantStatePostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_participant_state_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        participant_state = ParticipantStateIn()
        participant_state_service = ParticipantStateService()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(id=1))

    @mock.patch('graph_api_service.requests')
    def test_participant_state_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        participant_state = ParticipantStateIn()
        participant_state_service = ParticipantStateService()

        result = participant_state_service.save_participant_state(participant_state)

        self.assertEqual(result, ParticipantStateOut(errors={'error': 'test'}))
