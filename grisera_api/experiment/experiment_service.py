from graph_api_service import GraphApiService
from experiment.experiment_model import ExperimentIn, ExperimentsOut, BasicExperimentOut,ExperimentOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation

from typing import Union

class ExperimentService:
    """
    Abstract class to handle logic of experiments requests

    """

    def save_experiment(self, experiment: ExperimentIn):
        """
        Send request to graph api to create new experiment

        Args:
            experiment (ExperimentIn): Experiment to be added

        Returns:
            Result of request as experiment object
        """
        raise Exception("save_experiment not implemented yet")

    def get_experiments(self):
        """
        Send request to graph api to get experiments

        Returns:
            Result of request as list of experiments objects
        """
        raise Exception("get_experiments not implemented yet")

    def get_experiment(self, experiment_id: int):
        """
        Send request to graph api to get given experiment

        Args:
        experiment_id (int): Id of experiment

        Returns:
            Result of request as experiment object
        """
        raise Exception("get_experiment not implemented yet")

    def delete_experiment(self, experiment_id: Union[int, str]):
        """
        Send request to graph api to delete given experiment

        Args:
        experiment_id (int): Id of experiment

        Returns:
            Result of request as experiment object
        """
        raise Exception("delete_experiment not implemented yet")

    def update_experiment(self, experiment_id: int, experiment: ExperimentIn):
        """
        Send request to graph api to update given experiment

        Args:
        experiment_id (int): Id of experiment
        experiment (ExperimentIn): Properties to update

        Returns:
            Result of request as experiment object
        """
        raise Exception("update_experiment not implemented yet")
