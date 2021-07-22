from live_activity.live_activity_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_live_activity(*args, **kwargs):
    live_activity_out = LiveActivityOut(live_activity="muscles activity", id=1)
    return live_activity_out


class TestLiveActivityPost(unittest.TestCase):

    @mock.patch.object(LiveActivityService, 'save_live_activity')
    def test_live_activity_post_without_error(self, mock_service):
        mock_service.side_effect = return_live_activity
        response = Response()
        live_activity = LiveActivityIn(live_activity="muscles activity")
        live_activity_router = LiveActivityRouter()

        result = asyncio.run(live_activity_router
                             .create_live_activity(live_activity, response))

        self.assertEqual(result, LiveActivityOut(live_activity="muscles activity", id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(LiveActivityService, 'save_live_activity')
    def test_live_activity_post_with_error(self, mock_service):
        mock_service.return_value = LiveActivityOut(live_activity="muscles activity", errors={'errors': ['test']})
        response = Response()
        live_activity = LiveActivityIn(live_activity="muscles activity")
        live_activity_router = LiveActivityRouter()

        result = asyncio.run(live_activity_router
                             .create_live_activity(live_activity, response))

        self.assertEqual(response.status_code, 422)
