import unittest
import unittest.mock as mock

from ontology_api_service import OntologyApiService
from experiment.experiment_model import *
from experiment.experiment_service_ontology import ExperimentServiceOntology


class TestExperimentServicePost(unittest.TestCase):

    @mock.patch.object(OntologyApiService, 'add_instance')
    def test_save_experiment_without_error(self, add_instance_mock):
        model_id = 1
        experiment_name = "test"
        add_instance_mock.return_value = {'label': experiment_name, 'errors': None }
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment = ExperimentIn(experiment_name=experiment_name, additional_properties=additional_properties)
        experiment_service = ExperimentServiceOntology()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", additional_properties=additional_properties))
        add_instance_mock.assert_called_once_with(model_id, 'Experiment', 'test')

    @mock.patch.object(OntologyApiService, 'add_instance')
    def test_save_experiment_with_error(self, add_instance_mock):
        model_id = 1
        add_instance_mock.return_value = {'label': None, 'errors': "error" }
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment = ExperimentIn(experiment_name="test", additional_properties=additional_properties)
        experiment_service = ExperimentServiceOntology()

        result = experiment_service.save_experiment(experiment)

        self.assertEqual(result, ExperimentOut(experiment_name="test", additional_properties=additional_properties,
                                               errors='error'))
        add_instance_mock.assert_called_once_with(model_id, 'Experiment', 'test')