import json
import unittest
import unittest.mock as mock
from life_activity.life_activity_model import *
from life_activity.life_activity_service_graphdb import *
from requests import Response


class TestLifeActivityServicePost(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_life_activity_post_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        life_activity = LifeActivityIn(life_activity="movement")
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.save_life_activity(life_activity)

        self.assertEqual(result, LifeActivityOut(life_activity="movement", id=1))

    @mock.patch('graph_api_service.requests')
    def test_life_activity_post_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        life_activity = LifeActivityIn(life_activity="movement")
        life_activity_service = LifeActivityServiceGraphDB()

        result = life_activity_service.save_life_activity(life_activity)

        self.assertEqual(result, LifeActivityOut(life_activity="movement", errors={'error': 'test'}))
