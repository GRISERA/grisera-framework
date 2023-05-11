import asyncio
import unittest
import unittest.mock as mock

from activity.activity_model import BasicActivityOut
from activity.activity_service_graphdb import ActivityServiceGraphDB
from activity.activity_router import *
from fastapi import Response


class TestActivityRouterGet(unittest.TestCase):

    @mock.patch.object(ActivityServiceGraphDB, 'get_activity')
    def test_get_activity_without_error(self, get_activity_mock):
        dataset_name = "neo4j"
        activity_id = 1
        get_activity_mock.return_value = ActivityOut(activity='two-people', id=activity_id)
        response = Response()
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.get_activity(activity_id, response, dataset_name))

        self.assertEqual(result, ActivityOut(activity='two-people', id=activity_id, links=get_links(router)))

        get_activity_mock.assert_called_once_with(activity_id,dataset_name, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityServiceGraphDB, 'get_activity')
    def test_get_activity_with_error(self, get_activity_mock):
        dataset_name = "neo4j"
        get_activity_mock.return_value = ActivityOut(activity='two-people', errors={'errors': ['test']})
        response = Response()
        activity_id = 1
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.get_activity(activity_id, response, dataset_name))

        self.assertEqual(result,
                         ActivityOut(activity='two-people', errors={'errors': ['test']}, links=get_links(router)))
        get_activity_mock.assert_called_once_with(activity_id,dataset_name, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ActivityServiceGraphDB, 'get_activities')
    def test_get_activity_nodes_without_error(self, get_activities_mock):
        dataset_name = "neo4j"
        get_activities_mock.return_value = ActivitiesOut(activities=[
            BasicActivityOut(activity='two-people', id=1), BasicActivityOut(activity='group', id=2)])
        response = Response()
        activity_router = ActivityRouter()

        result = asyncio.run(activity_router.get_activities(response, dataset_name))

        self.assertEqual(result, ActivitiesOut(activities=[
            BasicActivityOut(activity='two-people', id=1), BasicActivityOut(activity='group', id=2)],
            links=get_links(router)))
        get_activities_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
