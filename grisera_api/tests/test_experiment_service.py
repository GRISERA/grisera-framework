import json
import unittest
import unittest.mock as mock
from experiment.experiment_model import *
from experiment.experiment_service import ExperimentService
from requests import Response


class TestExperimentPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_experiment_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        experiment = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(id=1, experiment_name="test"))

    @mock.patch('graph_api_service.requests')
    def test_experiment_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps(
            {'id': None, 'properties': {'experiment_name': 'test'}, "errors": {'error': 'test'},
             'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        experiment = ExperimentIn(experiment_name="test")
        experiment_service = ExperimentService()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", errors={'error': 'test'}))
