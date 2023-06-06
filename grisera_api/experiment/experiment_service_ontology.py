from typing import Union

from experiment.experiment_model import ExperimentIn, ExperimentOut
from experiment.experiment_service import ExperimentService
from activity_execution.activity_execution_model import ActivityExecutionOut
from ontology_api_service import OntologyApiService


class ExperimentServiceOntology(ExperimentService):
    """
    Object to handle logic of experiments requests

    Attributes:
    ontology_api_service (ExperimentService): Service used to communicate with Ontology API
    """
    ontology_api_service = OntologyApiService()

    def get_experiment(self, experiment_label: Union[int, str], depth: int = 0):
        """
        Send request to ontology api to get given experiment
        Args:
            experiment_label (int | str): label of experiment
            depth (int) : only for compatibility with graph_api, always set to 0
        Returns:
            Result of request as experiment object
        """
        model_id = 1

        instance_response_experiment = self.ontology_api_service.get_instance(model_id=model_id,
                                                                              class_name="Experiment",
                                                                              instance_label=experiment_label)
        if instance_response_experiment["errors"] is not None:
            experiment_result = {'experiment_name': experiment_label, 'errors': instance_response_experiment["errors"]}
            return ExperimentOut(**experiment_result)

        roles_response_experiment = self.ontology_api_service.get_roles(model_id, experiment_label)
        if roles_response_experiment["errors"] is not None:
            return ExperimentOut(ExperimentIn(experiment_label),
                                 errors=roles_response_experiment["errors"])

        a = None
        for prop in roles_response_experiment['roles']:
            if prop['role'] == 'hasScenario' and prop['instance_name'] == experiment_label:
                activity_execution_dictionary = {'id': prop['value']}
                a = ActivityExecutionOut(**activity_execution_dictionary)

        experiment_result = {'id': experiment_label,
                             'experiment_name': experiment_label,
                             'activity_executions': a}
        return ExperimentOut(**experiment_result)
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

        new_additional_properties = []

        errors = None

        for prop in experiment.additional_properties:
            response = self.ontology_api_service.add_role(model_id, prop.key, experiment.experiment_name, prop.value)
            if response["errors"] is not None:
                errors = f"[{prop.key} : {prop.value}]:" + response["errors"]
                break
            else:
                new_additional_properties.append(prop)

        experiment_label = instance_response_experiment["label"]
        experiment.__dict__.update({'experiment_name': experiment_label})
        experiment.__dict__.update({'additional_properties': new_additional_properties})

        if errors is None:
            return ExperimentOut(**experiment.dict())
        else:
            return ExperimentOut(**experiment.dict(), errors=errors)

    def update_experiment(self, experiment_id: int, experiment: ExperimentIn):
        """
        Send request to graph api to update given experiment

        Args:
        experiment_id (int): Id of experiment
        experiment (ExperimentIn): Properties to update

        Returns:
            Result of request as experiment object
        """
        model_id = 1
        get_response = self.get_experiment(experiment_id)

        if get_response.dict()["errors"] is not None:
            return ExperimentOut(**experiment.dict(), errors=get_response.dict()["errors"])

        self.ontology_api_service.delete_roles(model_id, experiment.experiment_name)

        new_additional_properties = []

        errors = None

        for prop in experiment.additional_properties:
            response = self.ontology_api_service.add_role(model_id, prop.key, experiment.experiment_name, prop.value)
            if response["errors"] is not None:
                errors = f"[{prop.key} : {prop.value}]:" + response["errors"]
                break
            else:
                new_additional_properties.append(prop)

        experiment_result = {'activity_executions': []}
        experiment_result.update(experiment.dict())
        experiment_result.update({'additional_properties': new_additional_properties})

        if errors is None:
            return ExperimentOut(**experiment_result)
        else:
            return ExperimentOut(**experiment_result, errors=errors)
          
    def delete_experiment(self, experiment_id: str):
        """
        Send request to ontology api to delete an experiment
        Args:

        Returns:
             Result of request as experiment object
        """
        model_id = 1
        instance_label = experiment_id
        response = self.ontology_api_service.delete_instance(model_id, "Experiment", instance_label)
        if response["errors"] is not None:
            return ExperimentOut(experiment_name=instance_label, errors=response["errors"])
        return ExperimentOut(experiment_name=response["label"])       
