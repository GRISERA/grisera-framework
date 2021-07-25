import asyncio
import unittest
import unittest.mock as mock

from activity.activity_model import ActivityIn, ActivityOut
from scenario.scenario_router import *


class TestScenarioRouter(unittest.TestCase):

    @mock.patch.object(ScenarioService, 'save_scenario')
    def test_create_scenario_without_error(self, save_scenario_mock):
        save_scenario_mock.return_value = ScenarioOut(experiment_id=2, activities=[ActivityOut(identifier=1)], id=1)
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activities=[ActivityIn(identifier=1)])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result, ScenarioOut(experiment_id=2, activities=[ActivityOut(identifier=1)], id=1,
                                             links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioService, 'save_scenario')
    def test_create_scenario_with_error(self, save_scenario_mock):
        save_scenario_mock.return_value = ScenarioOut(experiment_id=2, activities=[ActivityIn(identifier=1)],
                                                      errors={'errors': ['test']})
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activities=[ActivityIn(identifier=1)])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result,  ScenarioOut(experiment_id=2, activities=[ActivityOut(identifier=1)],
                                              errors={'errors': ['test']}, links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(ScenarioService, 'add_activity')
    def test_add_activity_without_error(self, add_activity_mock):
        add_activity_mock.return_value = ActivityOut(identifier=2, id=1)
        response = Response()
        activity = ActivityIn(identifier=2)
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity(1, activity, response))

        self.assertEqual(result, ActivityOut(identifier=2, id=1, links=get_links(router)))
        add_activity_mock.assert_called_once_with(1, activity)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioService, 'add_activity')
    def test_add_activity_with_error(self, add_activity_mock):
        add_activity_mock.return_value = ActivityOut(identifier=2, errors={'errors': ['test']})
        response = Response()
        activity = ActivityIn(identifier=2)
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity(1, activity, response))

        self.assertEqual(result, ActivityOut(identifier=2, errors={'errors': ['test']}, links=get_links(router)))
        add_activity_mock.assert_called_once_with(1, activity)
        self.assertEqual(response.status_code, 422)
