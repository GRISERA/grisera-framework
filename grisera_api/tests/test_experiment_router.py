import asyncio
import unittest
import unittest.mock as mock

from experiment.experiment_router import *


def return_experiment(*args, **kwargs):
    experiment_out = ExperimentOut(id=1, experiment_name="test")
    return experiment_out


class TestExperimentRouter(unittest.TestCase):

    @mock.patch.object(ExperimentService, 'save_experiment')
    def test_create_experiment_without_error(self, save_experiment_mock):
        save_experiment_mock.side_effect = return_experiment
        response = Response()
        experiment = ExperimentIn(id=1, experiment_name="test")
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.create_experiment(experiment, response))

        self.assertEqual(result, ExperimentOut(id=1, experiment_name="test", links=get_links(router)))
        save_experiment_mock.assert_called_once_with(experiment)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentService, 'save_experiment')
    def test_create_experiment_with_error(self, save_experiment_mock):
        save_experiment_mock.return_value = ExperimentOut(experiment_name="test", errors={'errors': ['test']})
        response = Response()
        experiment = ExperimentIn(id=1, experiment_name="test")
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.create_experiment(experiment, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test",
                                               errors={'errors': ['test']}, links=get_links(router)))
        save_experiment_mock.assert_called_once_with(experiment)
        self.assertEqual(response.status_code, 422)
