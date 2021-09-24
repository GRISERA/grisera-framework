from graph_api_service import GraphApiService
from activity.activity_service import ActivityService
from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut


class ActivityExecutionService:
    """
    Object to handle logic of activities requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        activity_service (ActivityService): Service used to communicate with Activity
    """
    graph_api_service = GraphApiService()
    activity_service = ActivityService()

    def save_activity_execution(self, activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to create new activity execution

        Args:
            activity_execution (ActivityExecutionIn): Activity Execution to be added

        Returns:
            Result of request as activity execution object
        """
        node_response = self.graph_api_service.create_node("ActivityExecution")

        if node_response["errors"] is not None:
            return ActivityExecutionOut(identifier=activity_execution.identifier, activity=activity_execution.activity,
                                        errors=node_response["errors"])

        activity_execution_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(activity_execution_id, activity_execution)
        if properties_response["errors"] is not None:
            return ActivityExecutionOut(identifier=activity_execution.identifier, activity=activity_execution.activity,
                                        errors=properties_response["errors"])

        activities = self.activity_service.get_activities().activities
        activity_id = next(activity.id for activity in activities
                           if activity.activity == activity_execution.activity)
        self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                    end_node=activity_id, name="hasActivity")

        return ActivityExecutionOut(identifier=activity_execution.identifier, activity=activity_execution.activity,
                                    name=activity_execution.name, layout=activity_execution.layout,
                                    id=activity_execution_id,
                                    additional_properties=activity_execution.additional_properties)
