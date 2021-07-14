from graph_api_service import GraphApiService
from activity.activity_model import ActivityIn, ActivityOut


class ActivityService:
    """
    Object to handle logic of activities requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_activity(self, activity: ActivityIn):
        """
        Send request to graph api to create new activity

        Args:
            activity (ActivityIn): Activity to be added

        Returns:
            Result of request as activity object
        """
        node_response = self.graph_api_service.create_node("Activity")

        if node_response["errors"] is not None:
            return ActivityOut(identifier=activity.identifier, errors=node_response["errors"])

        activity_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(activity_id, activity)
        if properties_response["errors"] is not None:
            return ActivityOut(identifier=activity.identifier, errors=properties_response["errors"])

        return ActivityOut(identifier=activity.identifier, name=activity.name, type=activity.type,
                           layout=activity.layout, id=activity_id, additional_properties=activity.additional_properties)
