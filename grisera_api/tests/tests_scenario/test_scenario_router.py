import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut
from scenario.scenario_router import *


class TestScenarioRouter(unittest.TestCase):

    @mock.patch.object(ScenarioService, 'save_scenario')
    def test_create_scenario_without_error(self, save_scenario_mock):
        save_scenario_mock.return_value = ScenarioOut(experiment_id=2, activity_executions=[ActivityExecutionOut(activity='group')], id=1)
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activity_executions=[ActivityExecutionIn(activity='group')])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result, ScenarioOut(experiment_id=2, activity_executions=[ActivityExecutionOut(activity='group')], id=1,
                                             links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioService, 'save_scenario')
    def test_create_scenario_with_error(self, save_scenario_mock):
        save_scenario_mock.return_value = ScenarioOut(experiment_id=2,
                                                      activity_executions=[ActivityExecutionIn(activity='group')],
                                                      errors={'errors': ['test']})
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activity_executions=[ActivityExecutionIn(activity='group')])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result,  ScenarioOut(experiment_id=2,
                                              activity_executions=[ActivityExecutionOut(activity='group')],
                                              errors={'errors': ['test']}, links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(ScenarioService, 'add_activity_execution')
    def test_add_activity_execution_without_error(self, add_activity_execution_mock):
        add_activity_execution_mock.return_value = ActivityExecutionOut(activity='group',  id=1)
        response = Response()
        activity_execution = ActivityExecutionIn(activity='group')
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity_execution(1, activity_execution, response))

        self.assertEqual(result, ActivityExecutionOut(activity='group',  id=1, links=get_links(router)))
        add_activity_execution_mock.assert_called_once_with(1, activity_execution)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioService, 'add_activity_execution')
    def test_add_activity_execution_with_error(self, add_activity_execution_mock):
        add_activity_execution_mock.return_value = ActivityExecutionOut(activity='group',  errors={'errors': ['test']})
        response = Response()
        activity_execution = ActivityExecutionIn(activity='group')
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity_execution(1, activity_execution, response))

        self.assertEqual(result, ActivityExecutionOut(activity='group',  errors={'errors': ['test']}, links=get_links(router)))
        add_activity_execution_mock.assert_called_once_with(1, activity_execution)
        self.assertEqual(response.status_code, 422)