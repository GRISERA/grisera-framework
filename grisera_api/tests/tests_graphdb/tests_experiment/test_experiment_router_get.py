import asyncio
import unittest
import unittest.mock as mock
from experiment.experiment_router import *
from experiment.experiment_model import BasicExperimentOut
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from property.property_model import PropertyIn


class TestExperimentRouterGet(unittest.TestCase):

    @mock.patch.object(ExperimentServiceGraphDB, 'get_experiment')
    def test_get_experiment_without_error(self, get_experiment_mock):
        experiment_id = 1
        get_experiment_mock.return_value = ExperimentOut(experiment_name="test",
                                                         additional_properties=[PropertyIn(key="test", value="test")],
                                                         id=experiment_id)
        response = Response()
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.get_experiment(experiment_id, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test",
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               id=experiment_id, links=get_links(router)))
        get_experiment_mock.assert_called_once_with(experiment_id, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentServiceGraphDB, 'get_experiment')
    def test_get_experiment_with_error(self, get_experiment_mock):
        get_experiment_mock.return_value = ExperimentOut(experiment_name="test",
                                                         additional_properties=[PropertyIn(key="test", value="test")],
                                                         errors={'errors': ['test']})
        response = Response()
        experiment_id = 1
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.get_experiment(experiment_id, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test",
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               errors={'errors': ['test']},  links=get_links(router)))
        get_experiment_mock.assert_called_once_with(experiment_id, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ExperimentServiceGraphDB, 'get_experiments')
    def test_get_experiments_without_error(self, get_experiments_mock):
        get_experiments_mock.return_value = ExperimentsOut(experiments=[
            BasicExperimentOut(experiment_name="test", id=1),
            BasicExperimentOut(experiment_name="test2", id=2)])
        response = Response()
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.get_experiments(response))

        self.assertEqual(result, ExperimentsOut(experiments=[
            BasicExperimentOut(experiment_name="test", id=1),
            BasicExperimentOut(experiment_name="test2", id=2)],
            links=get_links(router)))
        get_experiments_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
