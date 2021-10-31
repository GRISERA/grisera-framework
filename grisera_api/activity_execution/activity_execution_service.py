from graph_api_service import GraphApiService
from activity.activity_service import ActivityService
from arrangement.arrangement_service import ArrangementService
from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut


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
            activity_execution (ActivityExecutionIn): Activity Execution to be added

        Returns:
            Result of request as activity execution object
        """
        node_response = self.graph_api_service.create_node("ActivityExecution")

        if node_response["errors"] is not None:
            return ActivityExecutionOut(activity=activity_execution.activity,
                                        arrangement_type=activity_execution.arrangement_type,
                                        arrangement_distance=activity_execution.arrangement_distance,
                                        errors=node_response["errors"])

        activity_execution_id = node_response["id"]

        activities = self.activity_service.get_activities().activities
        activity_id = next(activity.id for activity in activities
                           if activity.activity == activity_execution.activity)
        self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                    end_node=activity_id, name="hasActivity")

        arrangements = self.arrangement_service.get_arrangements().arrangements
        arrangement_id, arrangement_distance = \
            next((arrangement.id, arrangement.arrangement_distance) for arrangement in arrangements
                 if arrangement.arrangement_type == activity_execution.arrangement_type and
                 arrangement.arrangement_distance == activity_execution.arrangement_distance)

        self.graph_api_service.create_relationships(start_node=activity_execution_id,
                                                    end_node=arrangement_id, name="hasArrangement")

        activity_execution.arrangement_distance = None

        properties_response = self.graph_api_service.create_properties(activity_execution_id, activity_execution)
        if properties_response["errors"] is not None:
            return ActivityExecutionOut(activity=activity_execution.activity,
                                        arrangement_type=activity_execution.arrangement_type,
                                        arrangement_distance=activity_execution.arrangement_distance,
                                        errors=properties_response["errors"])

        return ActivityExecutionOut(activity=activity_execution.activity,
                                    arrangement_type=activity_execution.arrangement_type,
                                    arrangement_distance=activity_execution.arrangement_distance,
                                    id=activity_execution_id,
                                    additional_properties=activity_execution.additional_properties)
