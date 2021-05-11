from activity.activity_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_activity(*args, **kwargs):
    activity_out = ActivityOut(identifier=2, id=1)
    return activity_out


class TestActivityPost(unittest.TestCase):

    @mock.patch.object(ActivityService, 'save_activity')
    def test_activity_post_without_error(self, mock_service):
        mock_service.side_effect = return_activity
        response = Response()
        activity = ActivityIn(identifier=2)
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.create_activity(activity, response))

        self.assertEqual(result, ActivityOut(identifier=2, id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityService, 'save_activity')
    def test_activity_post_with_error(self, mock_service):
        mock_service.return_value = ActivityOut(identifier=2, errors={'errors': ['test']})
        response = Response()
        activity = ActivityIn(identifier=2)
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.create_activity(activity, response))

        self.assertEqual(response.status_code, 422)
