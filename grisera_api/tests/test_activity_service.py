import json
import unittest
import unittest.mock as mock
from activity.activity_model import *
from activity.activity_service import ActivityService
from requests import Response


class TestActivityPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_activity_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        activity = ActivityIn(identifier=2)
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(identifier=2, id=1))

    @mock.patch('graph_api_service.requests')
    def test_activity_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        activity = ActivityIn(identifier=2)
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(identifier=2, errors={'error': 'test'}))
