import asyncio
import unittest
import unittest.mock as mock
from experiment.experiment_router import *
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from property.property_model import PropertyIn


class TestExperimentRouterPut(unittest.TestCase):

    @mock.patch.object(ExperimentServiceGraphDB, 'update_experiment')
    def test_update_experiment_without_error(self, update_experiment_mock):
        dataset_name = "neo4j"
        experiment_id = 1
        update_experiment_mock.return_value = ExperimentOut(experiment_name="test",
                                                            additional_properties=[PropertyIn(key="test", value="test")],
                                                            id=experiment_id)
        response = Response()
        experiment = ExperimentIn(experiment_name="test", additional_properties=[PropertyIn(key="test", value="test")])
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.update_experiment(experiment_id, experiment, response, dataset_name))

        self.assertEqual(result, ExperimentOut(experiment_name="test",
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               id=experiment_id, links=get_links(router)))
        update_experiment_mock.assert_called_once_with(experiment_id, experiment, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentServiceGraphDB, 'update_experiment')
    def test_update_experiment_with_error(self, update_experiment_mock):
        dataset_name = "neo4j"
        experiment_id = 1
        update_experiment_mock.return_value = ExperimentOut(experiment_name="test", errors={'errors': ['test']})
        response = Response()
        experiment = ExperimentIn(experiment_name="test")
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.update_experiment(experiment_id, experiment, response, dataset_name))

        self.assertEqual(result, ExperimentOut(experiment_name="test", errors={'errors': ['test']},
                                               links=get_links(router)))
        update_experiment_mock.assert_called_once_with(experiment_id, experiment, dataset_name)
        self.assertEqual(response.status_code, 404)
