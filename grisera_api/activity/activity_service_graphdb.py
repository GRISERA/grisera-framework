from typing import Union

from graph_api_service import GraphApiService
from activity.activity_model import ActivityIn, ActivityOut, ActivitiesOut, BasicActivityOut
from activity.activity_service import ActivityService
from models.not_found_model import NotFoundByIdModel
from helpers import create_stub_from_response


class ActivityServiceGraphDB(ActivityService):
    """
    Object to handle logic of activity requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.activity_execution_service = None

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

    def get_activity(self, activity_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given activity
        Args:
            depth(int): specifies how many related entities will be traversed to create the response
            activity_id (int | str): identity of activity
        Returns:
            Result of request as activity object
        """
        get_response = self.graph_api_service.get_node(activity_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=activity_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Activity":
            return NotFoundByIdModel(id=activity_id, errors="Node not found.")

        activity = create_stub_from_response(get_response, properties=['activity'])

        if depth != 0:
            activity['activity_executions'] = []
            relations_response = self.graph_api_service.get_node_relationships(activity_id)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == str(activity_id) and relation["name"] == "hasActivity":
                    activity['activity_executions']. \
                        append(
                        self.activity_execution_service.get_activity_execution(relation["start_node"], depth - 1))

            return ActivityOut(**activity)
        else:
            return BasicActivityOut(**activity)
