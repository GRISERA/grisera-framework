from typing import Union

from experiment.experiment_model import ExperimentIn, ExperimentOut
from experiment.experiment_service import ExperimentService
from models.relation_information_model import RelationInformation
from ontology_api_service import OntologyApiService


class ExperimentServiceOntology(ExperimentService):
    """
    Object to handle logic of experiments requests

    Attributes:
    ontology_api_service (ExperimentService): Service used to communicate with Ontology API
    """
    ontology_api_service = OntologyApiService()

    def save_experiment(self, experiment: ExperimentIn):
        """
        Send request to ontology api to add new experiment

        Args:
            model_id:
            experiment (ExperimentIn): Experiment to be added

        Returns:
            Result of request as experiment object
        """
        model_id = 1
        instance_response_experiment = self.ontology_api_service.add_instance(model_id, "Experiment",
                                                                              experiment.experiment_name)

        if instance_response_experiment["errors"] is not None:
            return ExperimentOut(**experiment.dict(), errors=instance_response_experiment["errors"])

        experiment_label = instance_response_experiment["label"]
        experiment.__dict__.update({'experiment_name': experiment_label})

        return ExperimentOut(**experiment.dict())

    def get_experiment(self, experiment_label: Union[int, str]):
        """
        Send request to ontology api to get given experiment

        Args:
            experiment_label (int | str): label of experiment

        Returns:
            Result of request as experiment object
        """
        model_id = 1
        instance_response_experiment = self.ontology_api_service.get_instance(model_id=model_id,
                                                                              class_name="Experiment",
                                                                              instance_label=experiment_label)

        if instance_response_experiment["errors"] is not None:
            return ExperimentOut(ExperimentIn(experiment_name=experiment_label),
                                 errors=instance_response_experiment["errors"])

        roles_response_experiment = self.ontology_api_service.get_roles(model_id=model_id,
                                                                        experiment_label=experiment_label)
        if roles_response_experiment["errors"] is not None:
            return ExperimentOut(ExperimentIn(experiment_name=experiment_label),
                                 errors=roles_response_experiment["errors"])
        relations = []
        for prop in roles_response_experiment:
            relations.append(RelationInformation(value=prop.value, second_node_id=0, relation_id=0, name=prop.role))

        reversed_roles_response_experiment = self.ontology_api_service.\
            get_reversed_roles(model_id=model_id, experiment_label=experiment_label)
        if reversed_roles_response_experiment["errors"] is not None:
            return ExperimentOut(ExperimentIn(experiment_name=experiment_label),
                                 errors=reversed_roles_response_experiment["errors"])
        reversed_relations = []
        for prop in roles_response_experiment:
            reversed_relations.append(
                RelationInformation(value=prop.instance_name, second_node_id=0, relation_id=0, name=prop.role))

        experiment_result = {'id': experiment_label, 'additional_properties': [], 'relations': relations,
                             'reversed_relations': reversed_relations}

        return ExperimentOut(**experiment_result)
