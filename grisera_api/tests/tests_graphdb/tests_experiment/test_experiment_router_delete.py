import asyncio
import unittest
import unittest.mock as mock
from grisera_api.experiment.experiment_router import *
from grisera_api.experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from grisera_api.property.property_model import PropertyIn


class TestExperimentRouterDelete(unittest.TestCase):

    @mock.patch.object(ExperimentServiceGraphDB, 'delete_experiment')
    def test_delete_experiment_without_error(self, delete_experiment_mock):
        experiment_id = 1
        delete_experiment_mock.return_value = ExperimentOut(experiment_name="test", id=experiment_id,
                                                            additional_properties=[
                                                                PropertyIn(key="test", value="test")])
        response = Response()
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.delete_experiment(experiment_id, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test", id=experiment_id,
                                               additional_properties=[PropertyIn(key="test", value="test")],
                                               links=get_links(router)))
        delete_experiment_mock.assert_called_once_with(experiment_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ExperimentServiceGraphDB, 'delete_experiment')
    def test_delete_experiment_with_error(self, delete_experiment_mock):
        delete_experiment_mock.return_value = ExperimentOut(experiment_name="test", errors={'errors': ['test']})
        response = Response()
        experiment_id = 1
        experiment_router = ExperimentRouter()

        result = asyncio.run(experiment_router.delete_experiment(experiment_id, response))

        self.assertEqual(result, ExperimentOut(experiment_name="test", errors={'errors': ['test']},
                                               links=get_links(router)))
        delete_experiment_mock.assert_called_once_with(experiment_id)
        self.assertEqual(response.status_code, 404)
