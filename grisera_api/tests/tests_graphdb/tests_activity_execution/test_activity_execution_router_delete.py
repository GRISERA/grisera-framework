import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_router import *
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB


class TestActivityExecutionRouterDelete(unittest.TestCase):

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'delete_activity_execution')
    def test_delete_activity_execution_without_error(self, delete_activity_execution_mock):
        database_name = "neo4j"
        activity_execution_id = 1
        delete_activity_execution_mock.return_value = ActivityExecutionOut(id=activity_execution_id)
        response = Response()
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.delete_activity_execution(activity_execution_id, response, database_name))

        self.assertEqual(result, ActivityExecutionOut(id=activity_execution_id, links=get_links(router)))
        delete_activity_execution_mock.assert_called_once_with(activity_execution_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'delete_activity_execution')
    def test_delete_activity_execution_with_error(self, delete_activity_execution_mock):
        database_name = "neo4j"
        delete_activity_execution_mock.return_value = ActivityExecutionOut(errors={'errors': ['test']})
        response = Response()
        activity_execution_id = 1
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.delete_activity_execution(activity_execution_id, response, database_name))

        self.assertEqual(result, ActivityExecutionOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_activity_execution_mock.assert_called_once_with(activity_execution_id, database_name)
        self.assertEqual(response.status_code, 404)