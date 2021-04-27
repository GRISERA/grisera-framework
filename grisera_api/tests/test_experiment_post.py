from experiment.experiment_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_experiment(*args, **kwargs):
    experiment_out = ExperimentOut(id=1, experiment_name="test")
    return experiment_out


class TestExperimentPost(unittest.TestCase):

    @mock.patch.object(ExperimentService, 'save_experiment')
    def test_experiment_post_without_error(self, mock_service):
        mock_service.side_effect = return_experiment
        response = Response()
        experiment = ExperimentIn(experiment_name="test")
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.create_experiment(experiment, response))

        self.assertEqual(result, ExperimentOut(id=1, experiment_name="test", links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentService, 'save_experiment')
    def test_experiment_post_with_error(self, mock_service):
        mock_service.return_value = ExperimentOut(experiment_name="test", errors={'errors': ['test']})
        response = Response()
        experiment = ExperimentIn(experiment_name="test")
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.create_experiment(experiment, response))

        self.assertEqual(response.status_code, 422)
