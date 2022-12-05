import asyncio
import unittest
import unittest.mock as mock

from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from property.property_model import PropertyIn
from experiment.experiment_router import *


class TestExperimentRouterPost(unittest.TestCase):

    @mock.patch.object(ExperimentServiceGraphDB, 'save_experiment')
    def test_create_experiment_without_error(self, save_experiment_mock):
        node_id = 1
        save_experiment_mock.return_value = ExperimentOut(experiment_name="test",
                                                          additional_properties=[PropertyIn(key="test", value="test")],
                                                          id=node_id)
        response = Response()
        experiment = ExperimentIn(experiment_name="test", additional_properties=[PropertyIn(key="test", value="test")])
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.create_experiment(experiment, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test",
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               id=node_id, links=get_links(router)))
        save_experiment_mock.assert_called_once_with(experiment)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentServiceGraphDB, 'save_experiment')
    def test_create_experiment_with_error(self, save_experiment_mock):
        save_experiment_mock.return_value = ExperimentOut(experiment_name="test",
                                                          additional_properties=[PropertyIn(key="test", value="test")],
                                                          errors="error")
        response = Response()
        experiment = ExperimentIn(experiment_name="test", additional_properties=[PropertyIn(key="test", value="test")])
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.create_experiment(experiment, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test",
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               errors="error", links=get_links(router)))
        save_experiment_mock.assert_called_once_with(experiment)
        self.assertEqual(response.status_code, 422)
