from experiment.experiment_model import ExperimentIn, ExperimentOut
from experiment.experiment_service import ExperimentService
from models.not_found_model import NotFoundByIdModel
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
        get_response = self.get_experiment(experiment.experiment_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.ontology_api_service.delete_roles(model_id, experiment.experiment_name)

        for prop in experiment.additional_properties:
            response = self.ontology_api_service.add_role(model_id, prop.key, experiment.experiment_name, prop.value)

        experiment_result = {'id': experiment_id, 'relations': get_response.relations,
                             'reversed_relations': get_response.reversed_relations}
        experiment_result.update(experiment.dict())

        return ExperimentOut(**experiment_result)
