import unittest
from unittest import mock

from experiment.experiment_model import ExperimentsOut, ExperimentOut
from experiment.experiment_service_ontology import ExperimentServiceOntology
from ontology_api_service import OntologyApiService


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
