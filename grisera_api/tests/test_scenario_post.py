from scenario.scenario_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_scenario(*args, **kwargs):
    return ScenarioOut(id=1, experiment_id=3, activities=[])


class TestScenarioPost(unittest.TestCase):

    @mock.patch.object(ScenarioService, 'save_scenario')
    def test_scenario_post_without_error(self, mock_service):
        mock_service.side_effect = return_scenario
        response = Response()
        scenario = ScenarioIn(experiment_id=3, activities=[])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result, ScenarioOut(experiment_id=3, activities=[], links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioService, 'save_scenario')
    def test_scenario_post_with_error(self, mock_service):
        mock_service.return_value = ScenarioOut(experiment_id=3, activities=[], errors={'errors': ['test']})
        response = Response()
        scenario = ScenarioIn(experiment_id=3, activities=[])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(response.status_code, 422)
