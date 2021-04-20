from graph_api_service import GraphApiService
from experiment.experiment_model import ExperimentIn, ExperimentOut


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
        node_response = self.graph_api_service.create_node("Experiment")

        if node_response["errors"] is not None:
            return ExperimentOut(name=experiment.name, errors=node_response["errors"])

        experiment_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(experiment_id, experiment)
        if properties_response["errors"] is not None:
            return ExperimentOut(name=experiment.name, errors=properties_response["errors"])

        return ExperimentOut(name=experiment.name, id=experiment_id)
