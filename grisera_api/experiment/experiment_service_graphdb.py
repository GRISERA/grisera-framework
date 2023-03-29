from experiment.experiment_service import ExperimentService
from graph_api_service import GraphApiService
from experiment.experiment_model import ExperimentIn, ExperimentsOut, BasicExperimentOut,ExperimentOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ExperimentServiceGraphDB(ExperimentService):
    """
    Object to handle logic of experiments requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()
    
    def save_experiment(self, experiment: ExperimentIn, database_name: str):
        """
        Send request to graph api to create new experiment

        Args:
            experiment (ExperimentIn): Experiment to be added

        Returns:
            Result of request as experiment object
        """
        node_response_experiment = self.graph_api_service.create_node("Experiment", database_name)

        print("###################RESPONSE: {}".format(node_response_experiment))


        if node_response_experiment["errors"] is not None:
            return ExperimentOut(**experiment.dict(), errors=node_response_experiment["errors"])

        experiment_id = node_response_experiment["id"]
        properties_response = self.graph_api_service.create_properties(experiment_id, experiment, database_name)
        if properties_response["errors"] is not None:
            return ExperimentOut(**experiment.dict(), errors=properties_response["errors"])

        return ExperimentOut(**experiment.dict(), id=experiment_id)

    def get_experiments(self, database_name: str):
        """
        Send request to graph api to get experiments

        Returns:
            Result of request as list of experiments objects
        """
        get_response = self.graph_api_service.get_nodes("Experiment", database_name)



        experiments = []

        for experiment_node in get_response["nodes"]:
            properties = {'id': experiment_node['id'], 'additional_properties': []}
            for property in experiment_node["properties"]:
                if property["key"] == "experiment_name":
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            experiment = BasicExperimentOut(**properties)  # TODO fix the error
            experiments.append(experiment)

        return ExperimentsOut(experiments=experiments)

    def get_experiment(self, experiment_id: int, database_name: str):
        """
        Send request to graph api to get given experiment

        Args:
        experiment_id (int): Id of experiment

        Returns:
            Result of request as experiment object
        """
        get_response = self.graph_api_service.get_node(experiment_id, database_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=experiment_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Experiment":
            return NotFoundByIdModel(id=experiment_id, errors="Node not found.")

        experiment = {'id': get_response['id'], 'additional_properties': [], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] == "experiment_name":
                experiment[property["key"]] = property["value"]
            else:
                experiment['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(experiment_id, database_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == experiment_id:
                experiment['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                   name=relation["name"], relation_id=relation["id"]))
            else:
                experiment['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                            name=relation["name"],
                                                                            relation_id=relation["id"]))

        return ExperimentOut(**experiment)

    def delete_experiment(self, experiment_id: int, database_name: str):
        """
        Send request to graph api to delete given experiment

        Args:
        experiment_id (int): Id of experiment

        Returns:
            Result of request as experiment object
        """
        get_response = self.get_experiment(experiment_id, database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(experiment_id, database_name)
        return get_response

    def update_experiment(self, experiment_id: int, experiment: ExperimentIn, database_name: str):
        """
        Send request to graph api to update given experiment

        Args:
        experiment_id (int): Id of experiment
        experiment (ExperimentIn): Properties to update

        Returns:
            Result of request as experiment object
        """
        get_response = self.get_experiment(experiment_id, database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(experiment_id, database_name)
        self.graph_api_service.create_properties(experiment_id, experiment, database_name)

        experiment_result = {'id': experiment_id, 'relations': get_response.relations,
                             'reversed_relations': get_response.reversed_relations}
        experiment_result.update(experiment.dict())

        return ExperimentOut(**experiment_result)
