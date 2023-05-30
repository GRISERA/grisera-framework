import unittest
from unittest.mock import Mock

from experiment.experiment_model import ExperimentIn, ExperimentOut
from activity_execution.activity_execution_model import ActivityExecutionOut
from ontology_api_service import OntologyApiService
from experiment.experiment_service_ontology import ExperimentServiceOntology


class ExperimentServiceOntologyTestCase(unittest.TestCase):
    def test_get_experiment_with_valid_label(self):
        ontology_api_service = Mock(spec=OntologyApiService)
        experiment_service = ExperimentServiceOntology()
        experiment_service.ontology_api_service = ontology_api_service
        instance_response = {"errors": None, "instance_name": "e1"}
        roles_response = {"errors": None, "roles": [{
                    "role": "hasScenario",
                    "value": "ae1",
                    "instance_name": "e1"}]}
        ontology_api_service.get_instance.return_value = instance_response
        ontology_api_service.get_roles.return_value = roles_response
        result = experiment_service.get_experiment("e1")
        self.assertIsInstance(result, ExperimentOut)
        self.assertEqual(result.id, "e1")
        self.assertEqual(result.experiment_name, "e1")
        self.assertIsInstance(result.activity_executions, ActivityExecutionOut)
        self.assertEqual(result.activity_executions.id, "ae1")
        ontology_api_service.get_instance.assert_called_once_with(
            model_id=1,
            class_name="Experiment",
            instance_label="e1"
        )

    def test_get_experiment_with_invalid_label(self):
        ontology_api_service = Mock(spec=OntologyApiService)
        experiment_service = ExperimentServiceOntology()
        experiment_service.ontology_api_service = ontology_api_service
        instance_response = {
            "errors": "Experiment not found",
        }
        ontology_api_service.get_instance.return_value = instance_response
        result = experiment_service.get_experiment("e2")
        self.assertIsInstance(result, ExperimentOut)
        self.assertEqual(result.id, None)
        self.assertEqual(result.experiment_name, "e2")
        self.assertEqual(result.errors, "Experiment not found")

        ontology_api_service.get_instance.assert_called_once_with(
            model_id=1,
            class_name="Experiment",
            instance_label="e2"
        )
