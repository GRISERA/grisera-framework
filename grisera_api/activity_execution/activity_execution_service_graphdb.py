from activity_execution.activity_execution_service import ActivityExecutionService
from graph_api_service import GraphApiService
from activity.activity_service_graphdb import ActivityServiceGraphDB
from arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from activity_execution.activity_execution_model import ActivityExecutionPropertyIn, ActivityExecutionRelationIn, \
    ActivityExecutionIn, ActivityExecutionOut, ActivityExecutionsOut, BasicActivityExecutionOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ActivityExecutionServiceGraphDB(ActivityExecutionService):
    """
    Object to handle logic of activities requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_service (ActivityService): Service used to communicate with Activity
    arrangement_service (ArrangementService): Service used to communicate with Arrangement
    """
    graph_api_service = GraphApiService()
    activity_service = ActivityServiceGraphDB()
    arrangement_service = ArrangementServiceGraphDB()

    def save_activity_execution(self, activity_execution: ActivityExecutionIn, dataset_name: str):
        """
        Send request to graph api to create new activity execution

        Args:
            activity_execution (ActivityExecutionIn): Activity execution to be added

        Returns:
            Result of request as activity execution object
        """
        node_response = self.graph_api_service.create_node("`Activity Execution`", dataset_name)

        if node_response["errors"] is not None:
            return ActivityExecutionOut(**activity_execution.dict(), errors=node_response["errors"])

        activity_execution_id = node_response["id"]

        if activity_execution.activity_id is not None and \
                type(self.activity_service.get_activity(activity_execution.activity_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.activity_id,
                                                        name="hasActivity",
                                                        dataset_name=dataset_name)

        if activity_execution.arrangement_id is not None and \
                type(self.arrangement_service.get_arrangement(activity_execution.arrangement_id,dataset_name)) \
                is not NotFoundByIdModel:

            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.arrangement_id,
                                                        name="hasArrangement",
                                                        dataset_name=dataset_name)

        activity_execution.activity_id = activity_execution.arrangement_id = None
        self.graph_api_service.create_properties(activity_execution_id, activity_execution, dataset_name)

        return self.get_activity_execution(activity_execution_id, dataset_name)

    def get_activity_executions(self, dataset_name: str):
        """
        Send request to graph api to get activity executions

        Returns:
            Result of request as list of activity executions objects
        """
        get_response = self.graph_api_service.get_nodes("`Activity Execution`", dataset_name)

        activity_executions = []
        for activity_execution_node in get_response["nodes"]:
            properties = {'id': activity_execution_node['id'], 'additional_properties': []}
            for property in activity_execution_node["properties"]:
                properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            activity_execution = BasicActivityExecutionOut(**properties)
            activity_executions.append(activity_execution)

        return ActivityExecutionsOut(activity_executions=activity_executions)

    def get_activity_execution(self, activity_execution_id: int, dataset_name: str):
        """
        Send request to graph api to get given activity execution

        Args:
            activity_execution_id (int): Id of activity execution

        Returns:
            Result of request as activity execution object
        """
        get_response = self.graph_api_service.get_node(activity_execution_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=activity_execution_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Activity Execution":
            return NotFoundByIdModel(id=activity_execution_id, errors="Node not found.")

        activity_execution = {'id': get_response['id'], 'additional_properties': [], 'relations': [],
                              'reversed_relations': []}
        for property in get_response["properties"]:
            activity_execution['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(activity_execution_id, dataset_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == activity_execution_id:
                activity_execution['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                           name=relation["name"],
                                                                           relation_id=relation["id"]))
            else:
                activity_execution['reversed_relations'].append(
                    RelationInformation(second_node_id=relation["start_node"],
                                        name=relation["name"],
                                        relation_id=relation["id"]))

        return ActivityExecutionOut(**activity_execution)

    def delete_activity_execution(self, activity_execution_id: int, dataset_name: str):
        """
        Send request to graph api to delete given activity execution
        Args:
            activity_execution_id (int): Id of activity execution
        Returns:
            Result of request as activity execution object
        """
        get_response = self.get_activity_execution(activity_execution_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(activity_execution_id, dataset_name)
        return get_response

    def update_activity_execution(self, activity_execution_id: int, activity_execution: ActivityExecutionPropertyIn, dataset_name: str):
        """
        Send request to graph api to update given participant state
        Args:
            activity_execution_id (int): Id of participant state
            activity_execution (ActivityExecutionPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        get_response = self.get_activity_execution(activity_execution_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(activity_execution_id,dataset_name)
        self.graph_api_service.create_properties(activity_execution_id, activity_execution,dataset_name)

        activity_execution_result = {"id": activity_execution_id, "relations": get_response.relations,
                                     "reversed_relations": get_response.reversed_relations}
        activity_execution_result.update(activity_execution.dict())

        return ActivityExecutionOut(**activity_execution_result)

    def update_activity_execution_relationships(self, activity_execution_id: int,
                                                activity_execution: ActivityExecutionRelationIn, dataset_name: str):
        """
        Send request to graph api to update given activity execution relationships
        Args:
            activity_execution_id (int): Id of activity execution
            activity_execution (ActivityExecutionIn): Relationships to update
        Returns:
            Result of request as activity execution object
        """
        get_response = self.get_activity_execution(activity_execution_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if activity_execution.activity_id is not None and \
                type(self.activity_service.get_activity(activity_execution.activity_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.activity_id,
                                                        name="hasActivity",
                                                        dataset_name=dataset_name)
        if activity_execution.arrangement_id is not None and \
                type(self.arrangement_service.get_arrangement(activity_execution.arrangement_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.arrangement_id,
                                                        name="hasArrangement",
                                                        dataset_name=dataset_name)

        return self.get_activity_execution(activity_execution_id,dataset_name)
