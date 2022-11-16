from graph_api_service import GraphApiService
from activity.activity_model import ActivityIn, ActivityOut, ActivitiesOut, BasicActivityOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


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
        raise Exception("save_activity not implemented yet")
    def get_activities(self):
        """
        Send request to graph api to get all activities

        Returns:
            Result of request as list of activity objects
        """
        raise Exception("get_activities not implemented yet")
    def get_activity(self, activity_id: int):
        """
        Send request to graph api to get given activity
        Args:
            activity_id (int): Id of activity
        Returns:
            Result of request as activity object
        """
        raise Exception("get_activity not implemented yet")

