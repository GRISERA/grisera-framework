from graph_api_service import GraphApiService
from live_activity.live_activity_model import LiveActivityIn, LiveActivityOut, LiveActivitiesOut, BasicLiveActivityOut


class LiveActivityService:
    """
    Object to handle logic of live activity requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_live_activity(self, live_activity: LiveActivityIn):
        """
        Send request to graph api to create new live activity

        Args:
            live_activity (LiveActivityIn): Live activity to be added

        Returns:
            Result of request as live activity object
        """

        node_response = self.graph_api_service.create_node("`Live Activity`")

        if node_response["errors"] is not None:
            return LiveActivityOut(live_activity=live_activity.live_activity, errors=node_response["errors"])

        live_activity_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(live_activity_id, live_activity)
        if properties_response["errors"] is not None:
            return LiveActivityOut(errors=properties_response["errors"])

        return LiveActivityOut(live_activity=live_activity.live_activity, id=live_activity_id)

    def get_live_activities(self):
        """
        Send request to graph api to get all live activities

        Returns:
            Result of request as list of live activity objects
        """
        get_response = self.graph_api_service.get_nodes("`Live Activity`")
        if get_response["errors"] is not None:
            return LiveActivitiesOut(errors=get_response["errors"])
        live_activities = [BasicLiveActivityOut(id=live_activity["id"], live_activity=live_activity["properties"][0]["value"])
                           for live_activity in get_response["nodes"]]

        return LiveActivitiesOut(live_activities=live_activities)
