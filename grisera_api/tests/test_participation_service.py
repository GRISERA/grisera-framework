import json
import unittest
import unittest.mock as mock
from participation.participation_model import *
from participation.participation_service import ParticipationService
from requests import Response


class TestParticipationPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_participation_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        participation_service = ParticipationService()

        result = participation_service.save_participation()

        self.assertEqual(result, ParticipationOut(id=1))

    @mock.patch('graph_api_service.requests')
    def test_participation_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        participation_service = ParticipationService()

        result = participation_service.save_participation()

        self.assertEqual(result, ParticipationOut(errors={'error': 'test'}))
