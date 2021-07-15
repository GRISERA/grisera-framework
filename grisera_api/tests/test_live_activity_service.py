import json
import unittest
import unittest.mock as mock
from live_activity.live_activity_model import *
from live_activity.live_activity_service import *
from requests import Response


class TestLiveActivityService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_live_activity_post_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        live_activity = LiveActivityIn(live_activity="movement")
        live_activity_service = LiveActivityService()

        result = live_activity_service.save_live_activity(live_activity)

        self.assertEqual(result, LiveActivityOut(live_activity="movement", id=1))

    @mock.patch('graph_api_service.requests')
    def test_live_activity_post_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        live_activity = LiveActivityIn(live_activity="movement")
        live_activity_service = LiveActivityService()

        result = live_activity_service.save_live_activity(live_activity)

        self.assertEqual(result, LiveActivityOut(live_activity="movement", errors={'error': 'test'}))
