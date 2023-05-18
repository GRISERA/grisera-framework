from typing import Union

from activity_execution.activity_execution_service import ActivityExecutionService
from experiment.experiment_service import ExperimentService
from graph_api_service import GraphApiService
from experiment.experiment_model import ExperimentIn, ExperimentsOut, BasicExperimentOut, ExperimentOut
from helpers import create_stub_from_response
from models.not_found_model import NotFoundByIdModel


class ExperimentServiceGraphDB(ExperimentService):
    """
    Object to handle logic of experiments requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.activity_execution_service: ActivityExecutionService = None

    def save_experiment(self, experiment: ExperimentIn, dataset_name: str):
        """
        Send request to graph api to create new experiment

        Args:
            experiment (ExperimentIn): Experiment to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as experiment object
        """
        node_response_experiment = self.graph_api_service.create_node("Experiment", dataset_name)

        if node_response_experiment["errors"] is not None:
            return ExperimentOut(**experiment.dict(), errors=node_response_experiment["errors"])

        experiment_id = node_response_experiment["id"]
        properties_response = self.graph_api_service.create_properties(experiment_id, experiment, dataset_name)
        if properties_response["errors"] is not None:
            return ExperimentOut(**experiment.dict(), errors=properties_response["errors"])

        return ExperimentOut(**experiment.dict(), id=experiment_id)

    def get_experiments(self, dataset_name: str):
        """
        Send request to graph api to get experiments

        Args:
             dataset_name (str): name of dataset

        Returns:
            Result of request as list of experiments objects
        """
        get_response = self.graph_api_service.get_nodes("Experiment", dataset_name)

        experiments = []

        for experiment_node in get_response["nodes"]:
            properties = {'id': experiment_node['id'], 'additional_properties': []}
            for property in experiment_node["properties"]:
                if property["key"] == "experiment_name":
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            experiment = BasicExperimentOut(**properties)
            experiments.append(experiment)

        return ExperimentsOut(experiments=experiments)

    def get_experiment(self, experiment_id: Union[int, str], dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given experiment

        Args:
            experiment_id (int | str): identity of experiment
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_name (str): name of dataset

        Returns:
            Result of request as experiment object
        """

        get_response = self.graph_api_service.get_node(experiment_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=experiment_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Experiment":
            return NotFoundByIdModel(id=experiment_id, errors="Node not found.")

        experiment = create_stub_from_response(get_response, properties=['experiment_name'])

        if depth != 0:
            experiment["activity_executions"] = []

            relations_response = self.graph_api_service.get_node_relationships(experiment_id, dataset_name)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == experiment_id & relation["name"] == "hasScenario":
                    experiment['activity_executions'].append(
                        self.activity_execution_service.get_activity_execution(relation["start_node"], depth - 1))

            return ExperimentOut(**experiment)
        else:
            return BasicExperimentOut(**experiment)

    def delete_experiment(self, experiment_id: int, dataset_name: str):
        """
        Send request to graph api to delete given experiment

        Args:
            experiment_id (int): Id of experiment
            dataset_name (str): name of dataset

        Returns:
            Result of request as experiment object
        """
        get_response = self.get_experiment(experiment_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(experiment_id, dataset_name)
        return get_response

    def update_experiment(self, experiment_id: int, experiment: ExperimentIn, dataset_name: str):
        """
        Send request to graph api to update given experiment

        Args:
            experiment_id (int): Id of experiment
            experiment (ExperimentIn): Properties to update
            dataset_name (str): name of dataset

        Returns:
            Result of request as experiment object
        """
        get_response = self.get_experiment(experiment_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(experiment_id, dataset_name)
        self.graph_api_service.create_properties(experiment_id, experiment, dataset_name)

        experiment_result = {'id': experiment_id}
        experiment_result.update(experiment.dict())

        return BasicExperimentOut(**experiment_result)
