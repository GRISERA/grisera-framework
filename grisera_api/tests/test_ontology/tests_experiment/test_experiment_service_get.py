import unittest
from unittest import mock
from experiment.experiment_model import ExperimentIn, ExperimentOut, PropertyIn
from models.relation_information_model import RelationInformation
from ontology_api_service import OntologyApiService
from experiment.experiment_service_ontology import ExperimentServiceOntology


class TestExperimentServiceGet(unittest.TestCase):
    @mock.patch.object(OntologyApiService, 'get_reversed_roles')
    @mock.patch.object(OntologyApiService, 'get_roles')
    @mock.patch.object(OntologyApiService, 'get_instance')
    def test_get_experiment_without_error(self, get_instance_mock, get_roles_mock, get_reversed_roles_mock):
        model_id = 1
        class_name = "Experiment"
        role = "test"
        value = "test"
        instance_label = "test"
        return_list = [RelationInformation(value="test", second_node_id=0, relation_id=0, name="test")]
        get_instance_mock.return_value = {'label': instance_label, 'errors': None}
        get_roles_mock.return_value = {'roles': [{'role': role, 'instance_name': instance_label, 'value': value}],
                                       'errors': None}
        get_reversed_roles_mock.return_value = {'roles': [{'role': role, 'instance_name': value,
                                                           'value': instance_label}], 'errors': None}
        additional_properties = [PropertyIn(key='test', value='test')]
        experiment_service = ExperimentServiceOntology()
        result = experiment_service.get_experiment(instance_label)
        self.assertEqual(result, ExperimentOut(experiment_name=instance_label, additional_properties=[],
                                               relations=return_list, reversed_relations=return_list))
        get_instance_mock.assert_called_once_with(model_id=model_id, class_name=class_name,
                                                  instance_label=instance_label)
        get_roles_mock.assert_called_once_with(model_id, instance_label)
        get_reversed_roles_mock.assert_called_once_with(model_id, instance_label)
