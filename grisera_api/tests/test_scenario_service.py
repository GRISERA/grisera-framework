import unittest
import unittest.mock as mock
from scenario.scenario_model import *
from scenario.scenario_service import ScenarioService, ActivityService
from graph_api_service import GraphApiService


class TestScenarioService(unittest.TestCase):

    @mock.patch.object(ActivityService, 'save_activity')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_scenario_without_error(self, create_relationships_mock, save_activity_mock):
        id_node = 1
        activity_out = ActivityOut(identifier=1, id=2)
        save_activity_mock.return_value = activity_out
        create_relationships_mock.return_value = activity_out
        calls = [mock.call(2, 2, 'hasActivity')]
        scenario = ScenarioIn(experiment_id=2, activities=[ActivityIn(identifier=1)])
        scenario_router = ScenarioService()

        result = scenario_router.save_scenario(scenario)

        self.assertEqual(result, ScenarioOut(experiment_id=2, activities=[activity_out], id=id_node))
        create_relationships_mock.assert_has_calls(calls)


