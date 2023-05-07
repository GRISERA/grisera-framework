import asyncio
import unittest
import unittest.mock as mock
from experiment.experiment_router import *
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from property.property_model import PropertyIn


class TestExperimentRouterDelete(unittest.TestCase):

    @mock.patch.object(ExperimentServiceGraphDB, 'delete_experiment')
    def test_delete_experiment_without_error(self, delete_experiment_mock):
        dataset_name = "neo4j"
        experiment_id = 1
        delete_experiment_mock.return_value = ExperimentOut(experiment_name="test", id=experiment_id,
                                                            additional_properties=[PropertyIn(key="test", value="test")])
        response = Response()
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.delete_experiment(experiment_id, response, dataset_name))

        self.assertEqual(result, ExperimentOut(experiment_name="test", id=experiment_id,
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               links=get_links(router)))
        delete_experiment_mock.assert_called_once_with(experiment_id, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentServiceGraphDB, 'delete_experiment')
    def test_delete_experiment_with_error(self, delete_experiment_mock):
        dataset_name = "neo4j"
        delete_experiment_mock.return_value = ExperimentOut(experiment_name="test", errors={'errors': ['test']})
        response = Response()
        experiment_id = 1
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.delete_experiment(experiment_id, response, dataset_name))

        self.assertEqual(result, ExperimentOut(experiment_name="test", errors={'errors': ['test']},
                                               links=get_links(router)))
        delete_experiment_mock.assert_called_once_with(experiment_id, dataset_name)
        self.assertEqual(response.status_code, 404)
