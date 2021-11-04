import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_router import *


class TestActivityExecutionRouterPut(unittest.TestCase):

    @mock.patch.object(ActivityExecutionService, 'update_activity_execution_relationships')
    def test_update_activity_execution_relationships_without_error(self, update_activity_execution_relationships_mock):
        id_node = 1
        update_activity_execution_relationships_mock.return_value = ActivityExecutionOut(id=id_node)
        response = Response()
        activity_execution_in = ActivityExecutionIn(activity_id=2, arrangement_id=3)
        activity_execution_out = ActivityExecutionOut(id=id_node, links=get_links(router))
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.
                             update_activity_execution_relationships(id_node, activity_execution_in, response))

        self.assertEqual(result, activity_execution_out)
        update_activity_execution_relationships_mock.assert_called_once_with(id_node, activity_execution_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityExecutionService, 'update_activity_execution_relationships')
    def test_update_activity_execution_relationships_with_error(self, update_activity_execution_relationships_mock):
        id_node = 1
        update_activity_execution_relationships_mock.return_value = ActivityExecutionOut(id=id_node, errors="error")
        response = Response()
        activity_execution_in = ActivityExecutionIn(activity_id=2, arrangement_id=3)
        activity_execution_out = ActivityExecutionOut(id=id_node, errors="error", links=get_links(router))
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.
                             update_activity_execution_relationships(id_node, activity_execution_in, response))

        self.assertEqual(result, activity_execution_out)
        update_activity_execution_relationships_mock.assert_called_once_with(id_node, activity_execution_in)
        self.assertEqual(response.status_code, 404)