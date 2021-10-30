import json
import unittest
import unittest.mock as mock
from activity.activity_model import *
from activity.activity_service import *
from requests import Response


class TestActivityService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_activity_post_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        activity = ActivityIn(activity="group")
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(activity="group", id=1))

    @mock.patch('graph_api_service.requests')
    def test_activity_post_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        activity = ActivityIn(activity="group")
        activity_service = ActivityService()

        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(activity="group", errors={'error': 'test'}))