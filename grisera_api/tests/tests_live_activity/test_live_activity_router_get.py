import asyncio
import unittest
import unittest.mock as mock
from live_activity.live_activity_router import *
from live_activity.live_activity_model import BasicLiveActivityOut
from property.property_model import PropertyIn


class TestLiveActivityRouterGet(unittest.TestCase):

    @mock.patch.object(LiveActivityService, 'get_live_activity')
    def test_get_live_activity_without_error(self, get_live_activity_mock):
        live_activity_id = 1
        get_live_activity_mock.return_value = LiveActivityOut(live_activity='url', id=live_activity_id)
        response = Response()
        live_activity_router = LiveActivityRouter()

        result = asyncio.run(live_activity_router.get_live_activity(live_activity_id, response))

        self.assertEqual(result, LiveActivityOut(live_activity='url', id=live_activity_id, links=get_links(router)))
        get_live_activity_mock.assert_called_once_with(live_activity_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(LiveActivityService, 'get_live_activity')
    def test_get_live_activity_with_error(self, get_live_activity_mock):
        get_live_activity_mock.return_value = LiveActivityOut(live_activity='url', errors={'errors': ['test']})
        response = Response()
        live_activity_id = 1
        live_activity_router = LiveActivityRouter()

        result = asyncio.run(live_activity_router.get_live_activity(live_activity_id, response))

        self.assertEqual(result, LiveActivityOut(live_activity='url', errors={'errors': ['test']},  links=get_links(router)))
        get_live_activity_mock.assert_called_once_with(live_activity_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(LiveActivityService, 'get_live_activities')
    def test_get_live_activity_nodes_without_error(self, get_live_activities_mock):
        get_live_activities_mock.return_value = LiveActivitiesOut(live_activities=[
            BasicLiveActivityOut(live_activity='url', id=1), BasicLiveActivityOut(live_activity='url2', id=2)])
        response = Response()
        live_activity_router = LiveActivityRouter()

        result = asyncio.run(live_activity_router.get_live_activities(response))

        self.assertEqual(result, LiveActivitiesOut(live_activities=[
            BasicLiveActivityOut(live_activity='url', id=1), BasicLiveActivityOut(live_activity='url2', id=2)],
            links=get_links(router)))
        get_live_activities_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
