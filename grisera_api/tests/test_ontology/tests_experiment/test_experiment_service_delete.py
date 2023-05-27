import unittest
import unittest.mock as mock

from ontology_api_service import OntologyApiService
from experiment.experiment_model import *
from experiment.experiment_service_ontology import ExperimentServiceOntology

class TestExperimentServiceDelete(unittest.TestCase):

    @mock.patch.object(OntologyApiService, 'delete_instance')
    def test_delete_experiment_without_error(self, delete_instance_mock):
        model_id = 1
        experiment_id = "JK"
        delete_instance_mock.return_value = {'instance_id': 'Test', 'label': experiment_id, 'errors': None}
        experiment_service = ExperimentServiceOntology()
        result = experiment_service.delete_experiment(experiment_id)
        self.assertEqual(result, ExperimentOut(experiment_name=experiment_id))
        delete_instance_mock.assert_called_once_with(model_id, 'Experiment', experiment_id)

    @mock.patch.object(OntologyApiService, 'delete_instance')
    def test_delete_experiment_with_error(self, delete_instance_mock):
        model_id = 1
        experiment_id = "JK"
        delete_instance_mock.return_value = {'instance_id': 'Test', 'label': experiment_id, 'errors': 'error'}
        experiment_service = ExperimentServiceOntology()
        result = experiment_service.delete_experiment(experiment_id)
        self.assertEqual(result, ExperimentOut(experiment_name=experiment_id, errors='error'))
        delete_instance_mock.assert_called_once_with(model_id, 'Experiment', experiment_id)

