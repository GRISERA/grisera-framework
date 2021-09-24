from graph_api_service import GraphApiService
from activity.activity_model import ActivityIn, ActivityOut, ActivitiesOut, BasicActivityOut


class ActivityService:
    """
    Object to handle logic of activity requests

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
            return ActivityOut(activity=activity.activity, errors=node_response["errors"])

        activity_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(activity_id, activity)
        if properties_response["errors"] is not None:
            return ActivityOut(activity=activity.activity, errors=properties_response["errors"])

        return ActivityOut(activity=activity.activity, id=activity_id)

    def get_activities(self):
        """
        Send request to graph api to get all activities

        Returns:
            Result of request as list of activity objects
        """
        get_response = self.graph_api_service.get_nodes("Activity")
        if get_response["errors"] is not None:
            return ActivitiesOut(errors=get_response["errors"])
        activities = [BasicActivityOut(id=activity["id"], activity=activity["properties"][0]["value"])
                      for activity in get_response["nodes"]]

        return ActivitiesOut(activities=activities)
