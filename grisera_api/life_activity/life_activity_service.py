from graph_api_service import GraphApiService
from life_activity.life_activity_model import LifeActivityIn, LifeActivityOut, LifeActivitiesOut, BasicLifeActivityOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class LifeActivityService:
    """
    Object to handle logic of life activity requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_life_activity(self, life_activity: LifeActivityIn):
        """
        Send request to graph api to create new life activity

        Args:
            life_activity (LifeActivityIn): Life activity to be added

        Returns:
            Result of request as life activity object
        """
        raise Exception("save_life_activity not implemented yet")

    def get_life_activities(self):
        """
        Send request to graph api to get all life activities

        Returns:
            Result of request as list of life activity objects
        """
        raise Exception("get_life_activities not implemented yet")

    def get_life_activity(self, life_activity_id: int):
        """
        Send request to graph api to get given life activity

        Args:
        life_activity_id (int): Id of life activity

        Returns:
            Result of request as life activity object
        """
        raise Exception("get_life_activity not implemented yet")
