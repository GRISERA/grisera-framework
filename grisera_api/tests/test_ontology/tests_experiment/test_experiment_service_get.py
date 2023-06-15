import unittest

from unittest import mock
from unittest.mock import Mock

from experiment.experiment_model import ExperimentIn, ExperimentOut, ExperimentsOut
from activity_execution.activity_execution_model import ActivityExecutionOut
from ontology_api_service import OntologyApiService
from experiment.experiment_service_ontology import ExperimentServiceOntology


class TestExperimentServiceGet(unittest.TestCase):

    @mock.patch.object(ExperimentServiceOntology, 'get_experiment')
    @mock.patch.object(OntologyApiService, 'get_instances')
    def test_get_experiments_without_error(self, get_instances_mock, get_experiment_mock):
        model_id = 1
        experiments = [ExperimentOut(id="AAA", experiment_name="AAA", activity_executions=[]),
                       ExperimentOut(id="BBB", experiment_name="BBB", activity_executions=[])]
        get_instances_mock.return_value = {'errors': None, 'instances': [{'instance_name': "AAA"},
                                                                         {'instance_name': "BBB"}]}
        get_experiment_mock.side_effect = [
            ExperimentOut(id="AAA", experiment_name="AAA", activity_executions=[]),
            ExperimentOut(id="BBB", experiment_name="BBB", activity_executions=[])
        ]

        experiment_service = ExperimentServiceOntology()
        result = experiment_service.get_experiments()

        self.assertEqual(result, ExperimentsOut(experiments=experiments))
        get_instances_mock.assert_called_once_with(model_id, 'Experiment')
        get_experiment_mock.assert_has_calls([
            mock.call('AAA'),
            mock.call('BBB')
        ])

    @mock.patch.object(OntologyApiService, 'get_instances')
    def test_get_experiments_with_error(self, get_instances_mock):
        model_id = 1
        get_instances_mock.return_value = {'errors': "ERROR", 'instances': [{'instance_name': "AAA"},
                                                                            {'instance_name': "BBB"}]}

        experiment_service = ExperimentServiceOntology()
        result = experiment_service.get_experiments()

        self.assertEqual(result, ExperimentsOut(errors="ERROR"))
        get_instances_mock.assert_called_once_with(model_id, 'Experiment')

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
