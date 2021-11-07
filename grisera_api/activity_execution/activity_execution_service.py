from graph_api_service import GraphApiService
from activity.activity_service import ActivityService
from arrangement.arrangement_service import ArrangementService
from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut, \
    ActivityExecutionsOut, BasicActivityExecutionOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ActivityExecutionService:
    """
    Object to handle logic of activities requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_service (ActivityService): Service used to communicate with Activity
    arrangement_service (ArrangementService): Service used to communicate with Arrangement
    """
    graph_api_service = GraphApiService()
    activity_service = ActivityService()
    arrangement_service = ArrangementService()

    def save_activity_execution(self, activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to create new activity execution

        Args:
            activity_execution (ActivityExecutionIn): Activity execution to be added

        Returns:
            Result of request as activity execution object
        """
        node_response = self.graph_api_service.create_node("`Activity Execution`")

        if node_response["errors"] is not None:
            return ActivityExecutionOut(errors=node_response["errors"])
        activity_execution_id = node_response["id"]

        if activity_execution.activity_id is not None and\
                type(self.activity_service.get_activity(activity_execution.activity_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.activity_id,
                                                        name="hasActivity")

        if activity_execution.arrangement_id is not None and\
                type(self.arrangement_service.get_arrangement(activity_execution.arrangement_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.arrangement_id,
                                                        name="hasArrangement")

        properties_response = self.graph_api_service.create_properties(activity_execution_id, activity_execution)
        if properties_response["errors"] is not None:
            return ActivityExecutionOut(errors=properties_response["errors"])

        return self.get_activity_execution(activity_execution_id)

    def get_activity_executions(self):
        """
        Send request to graph api to get activity executions

        Returns:
            Result of request as list of activity executions objects
        """
        get_response = self.graph_api_service.get_nodes("`Activity Execution`")
    
        activity_executions = []

        for activity_execution_node in get_response["nodes"]:
            properties = {'id': activity_execution_node['id']}
            for property in activity_execution_node["properties"]:
                if property["key"] == "age":
                    properties[property["key"]] = property["value"]
            activity_execution = BasicActivityExecutionOut(**properties)
            activity_executions.append(activity_execution)

        return ActivityExecutionsOut(activity_executions=activity_executions)

    def get_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to get given activity execution

        Args:
            activity_execution_id (int): Id of activity execution

        Returns:
            Result of request as activity execution object
        """
        get_response = self.graph_api_service.get_node(activity_execution_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=activity_execution_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Activity Execution":
            return NotFoundByIdModel(id=activity_execution_id, errors="Node not found.")

        activity_execution = {'id': get_response['id'], 'relations': [],
                              'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] == "age":
                activity_execution[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(activity_execution_id)

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

    def delete_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to delete given activity execution
        Args:
            activity_execution_id (int): Id of activity execution
        Returns:
            Result of request as activity execution object
        """
        get_response = self.get_activity_execution(activity_execution_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(activity_execution_id)
        return get_response

    def update_activity_execution_relationships(self, activity_execution_id: int,
                                                activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to update given activity execution
        Args:
            activity_execution_id (int): Id of activity execution
            activity_execution (ActivityExecutionIn): Relationships to update
        Returns:
            Result of request as activity execution object
        """
        get_response = self.get_activity_execution(activity_execution_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if activity_execution.activity_id is not None and \
                type(self.activity_service.get_activity(activity_execution.activity_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.activity_id,
                                                        name="hasActivity")
        if activity_execution.arrangement_id is not None and \
                type(self.arrangement_service.get_arrangement(activity_execution.arrangement_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                        end_node=activity_execution.arrangement_id,
                                                        name="hasArrangement")

        return self.get_activity_execution(activity_execution_id)
