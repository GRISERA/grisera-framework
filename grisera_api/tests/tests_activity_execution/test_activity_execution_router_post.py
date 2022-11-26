import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from participant.participant_model import ParticipantIn
from activity_execution.activity_execution_model import *
from activity_execution.activity_execution_router import *


class TestActivityExecutionRouterPost(unittest.TestCase):

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'save_activity_execution')
    def test_create_activity_execution_without_error(self, save_activity_execution_mock):
        save_activity_execution_mock.return_value = ActivityExecutionOut(id=1)
        response = Response()
        activity_execution = ActivityExecutionPropertyIn()
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.create_activity_execution(activity_execution, response))

        self.assertEqual(result, ActivityExecutionOut(id=1, links=get_links(router)))
        save_activity_execution_mock.assert_called_once_with(activity_execution)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'save_activity_execution')
    def test_create_activity_execution_with_error(self, save_activity_execution_mock):
        save_activity_execution_mock.return_value = ActivityExecutionOut(errors={'errors': ['test']})
        response = Response()
        activity_execution = ActivityExecutionPropertyIn()
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.create_activity_execution(activity_execution, response))

        self.assertEqual(result, ActivityExecutionOut(errors={'errors': ['test']}, links=get_links(router)))
        save_activity_execution_mock.assert_called_once_with(activity_execution)
        self.assertEqual(response.status_code, 422)
