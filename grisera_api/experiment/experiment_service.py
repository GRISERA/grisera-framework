from graph_api_service import GraphApiService
from experiment.experiment_model import ExperimentIn, ExperimentOut
from author.author_service import AuthorService, AuthorOut
from publication.publication_service import PublicationService


class ExperimentService:
    """
    Object to handle logic of experiments requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()
    
    def save_experiment(self, experiment: ExperimentIn):
        """
        Send request to graph api to create new experiment

        Args:
            experiment (ExperimentIn): Experiment to be added

        Returns:
            Result of request as experiment object
        """
        node_response_experiment = self.graph_api_service.create_node("Experiment")

        if node_response_experiment["errors"] is not None:
            return ExperimentOut(experiment_name=experiment.experiment_name, errors=node_response_experiment["errors"])

        experiment_id = node_response_experiment["id"]
        properties_response = self.graph_api_service.create_properties(experiment_id, experiment)
        if properties_response["errors"] is not None:
            return ExperimentOut(experiment_name=experiment.experiment_name, errors=properties_response["errors"])

        return ExperimentOut(experiment_name=experiment.experiment_name, id=experiment_id,
                             additional_properties=experiment.additional_properties)
