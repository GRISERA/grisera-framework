import asyncio
import unittest
import unittest.mock as mock

from activity.activity_router import *


def return_activity(*args, **kwargs):
    activity_out = ActivityOut(identifier=2, id=1)
    return activity_out


class TestActivityRouter(unittest.TestCase):

    @mock.patch.object(ActivityService, 'save_activity')
    def test_create_activity_without_error(self, save_activity_mock):
        save_activity_mock.side_effect = return_activity
        response = Response()
        activity = ActivityIn(identifier=2)
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.create_activity(activity, response))

        self.assertEqual(result, ActivityOut(identifier=2, id=1, links=get_links(router)))
        save_activity_mock.assert_called_once_with(activity)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityService, 'save_activity')
    def test_create_activity_with_error(self, save_activity_mock):
        save_activity_mock.return_value = ActivityOut(identifier=2, errors={'errors': ['test']})
        response = Response()
        activity = ActivityIn(identifier=2)
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.create_activity(activity, response))

        self.assertEqual(result, ActivityOut(identifier=2, errors={'errors': ['test']}, links=get_links(router)))
        save_activity_mock.assert_called_once_with(activity)
        self.assertEqual(response.status_code, 422)
