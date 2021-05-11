import json
import unittest
import unittest.mock as mock
from activity.activity_model import *
from scenario.scenario_model import *
from scenario.scenario_service import ScenarioService
from requests import Response


class TestScenarioPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_scenario_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        scenario = ScenarioIn(experiment_id=3, activities=[ActivityIn(identifier=0)])
        scenario_service = ScenarioService()

        result = scenario_service.save_scenario(scenario)

        self.assertEqual(result, ScenarioOut(experiment_id=3, activities=[ActivityOut(identifier=0, id=1)]))

    @mock.patch('graph_api_service.requests')
    def test_experiment_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps(
            {'id': None, 'properties': None, "errors": {'error': 'test'}, 'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        scenario = ScenarioIn(experiment_id=3, activities=[ActivityIn(identifier=0)])
        scenario_service = ScenarioService()

        result = scenario_service.save_scenario(scenario)

        self.assertEqual(result, ScenarioOut(experiment_id=3,
                                             activities=[ActivityOut(identifier=0, errors={'error': 'test'})]))
