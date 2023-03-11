import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut
from scenario.scenario_router import *
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB


class TestScenarioRouter(unittest.TestCase):

    @mock.patch.object(ScenarioServiceGraphDB, 'save_scenario')
    def test_create_scenario_without_error(self, save_scenario_mock):
        database_name = "neo4j"
        save_scenario_mock.return_value = ScenarioOut(experiment_id=2, activity_executions=
        [ActivityExecutionOut(activity='group', arrangement_type='personal group')], id=1)
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activity_executions=[ActivityExecutionIn(activity_id=1,
                                                                                        arrangement_id=3)])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response, database_name))

        self.assertEqual(result, ScenarioOut(experiment_id=2, activity_executions=
        [ActivityExecutionOut(activity='group', arrangement_type='personal group')], id=1,
                                             links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioServiceGraphDB, 'save_scenario')
    def test_create_scenario_with_error(self, save_scenario_mock):
        database_name = "neo4j"
        save_scenario_mock.return_value = ScenarioOut(experiment_id=2,
                                                      activity_executions=
                                                      [ActivityExecutionIn(activity_id=1, arrangement_id=3)],
                                                      errors={'errors': ['test']})
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activity_executions=
        [ActivityExecutionIn(activity_id=1, arrangement_id=3,)])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response, database_name))

        self.assertEqual(result, ScenarioOut(experiment_id=2,
                                             activity_executions=
                                             [ActivityExecutionOut(activity='group',
                                                                   arrangement_type='personal group')],
                                             errors={'errors': ['test']}, links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario, database_name)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(ScenarioServiceGraphDB, 'add_activity_execution')
    def test_add_activity_execution_without_error(self, add_activity_execution_mock):
        database_name = "neo4j"
        add_activity_execution_mock.return_value = ActivityExecutionOut(activity_id=1, arrangement_id=3, id=1)
        response = Response()
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3,)
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity_execution(1, activity_execution, response, database_name))

        self.assertEqual(result, ActivityExecutionOut(activity='group', arrangement_type='personal group',
                                                      id=1, links=get_links(router)))
        add_activity_execution_mock.assert_called_once_with(1, activity_execution, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioServiceGraphDB, 'add_activity_execution')
    def test_add_activity_execution_with_error(self, add_activity_execution_mock):
        database_name = "neo4j"
        add_activity_execution_mock.return_value = ActivityExecutionOut(activity_id=1, arrangement_id=3,
                                                                        errors={'errors': ['test']})
        response = Response()
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3,)
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity_execution(1, activity_execution, response, database_name))

        self.assertEqual(result, ActivityExecutionOut(activity='group', arrangement_type='personal group',
                                                      errors={'errors': ['test']}, links=get_links(router)))
        add_activity_execution_mock.assert_called_once_with(1, activity_execution, database_name)
        self.assertEqual(response.status_code, 422)
