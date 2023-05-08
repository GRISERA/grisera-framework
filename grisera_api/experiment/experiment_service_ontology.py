from experiment.experiment_model import ExperimentIn, ExperimentOut
from experiment.experiment_service import ExperimentService
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

        for prop in experiment.additional_properties:
            response = self.ontology_api_service.add_role(model_id, prop.key, experiment.experiment_name, prop.value)
            if response["errors"] is not None:
                return ExperimentOut(**experiment.dict(), errors=response["errors"])

        experiment_label = instance_response_experiment["label"]
        experiment.__dict__.update({'experiment_name': experiment_label})

        return ExperimentOut(**experiment.dict())