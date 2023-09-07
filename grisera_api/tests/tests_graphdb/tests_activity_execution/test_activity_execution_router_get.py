import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import *
from activity_execution.activity_execution_router import *
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB

"""TODO: expand unit test for get with depth different from  0"""


class TestActivityExecutionRouterGet(unittest.TestCase):

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'get_activity_execution')
    def test_get_activity_execution_without_error(self, get_activity_execution_mock):
        dataset_name = "neo4j"
        activity_execution_id = 1
        get_activity_execution_mock.return_value = ActivityExecutionOut(id=activity_execution_id)
        response = Response()
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.get_activity_execution(activity_execution_id, response, dataset_name))

        self.assertEqual(result, ActivityExecutionOut(id=activity_execution_id, links=get_links(router)))

        get_activity_execution_mock.assert_called_once_with(activity_execution_id,dataset_name, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'get_activity_execution')
    def test_get_activity_execution_with_error(self, get_activity_execution_mock):
        dataset_name = "neo4j"
        get_activity_execution_mock.return_value = ActivityExecutionOut(errors={'errors': ['test']})
        response = Response()
        activity_execution_id = 1
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.get_activity_execution(activity_execution_id, response, dataset_name))

        self.assertEqual(result, ActivityExecutionOut(errors={'errors': ['test']},
                                                      links=get_links(router)))
        get_activity_execution_mock.assert_called_once_with(activity_execution_id,dataset_name, 0)

        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'get_activity_executions')
    def test_get_activity_executions_without_error(self, get_activity_executions_mock):
        dataset_name = "neo4j"
        get_activity_executions_mock.return_value = ActivityExecutionsOut(activity_executions=[
            BasicActivityExecutionOut(id=1),
            BasicActivityExecutionOut(id=2)])
        response = Response()
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.get_activity_executions(response, dataset_name))

        self.assertEqual(result, ActivityExecutionsOut(activity_executions=[
            BasicActivityExecutionOut(id=1),
            BasicActivityExecutionOut(id=2)],
            links=get_links(router)))
        get_activity_executions_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
