from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from life_activity.life_activity_model import LifeActivityIn, LifeActivityOut, LifeActivitiesOut, BasicLifeActivityOut
from life_activity.life_activity_service import LifeActivityService
from models.not_found_model import NotFoundByIdModel
from observable_information.observable_information_service import ObservableInformationService


class LifeActivityServiceGraphDB(LifeActivityService):
    """
    Object to handle logic of life activity requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.observable_information_service: ObservableInformationService = None

    def save_life_activity(self, life_activity: LifeActivityIn):
        """
        Send request to graph api to create new life activity

        Args:
            life_activity (LifeActivityIn): Life activity to be added

        Returns:
            Result of request as life activity object
        """

        node_response = self.graph_api_service.create_node("Life_Activity")

        if node_response["errors"] is not None:
            return LifeActivityOut(life_activity=life_activity.life_activity, errors=node_response["errors"])

        life_activity_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(life_activity_id, life_activity)
        if properties_response["errors"] is not None:
            return LifeActivityOut(errors=properties_response["errors"])

        return LifeActivityOut(life_activity=life_activity.life_activity, id=life_activity_id)

    def get_life_activities(self):
        """
        Send request to graph api to get all life activities

        Returns:
            Result of request as list of life activity objects
        """
        get_response = self.graph_api_service.get_nodes("Life_Activity")
        if get_response["errors"] is not None:
            return LifeActivitiesOut(errors=get_response["errors"])
        life_activities = [BasicLifeActivityOut(id=life_activity["id"],
                                                life_activity=life_activity["properties"][0]["value"])
                           for life_activity in get_response["nodes"]]

        return LifeActivitiesOut(life_activities=life_activities)

    def get_life_activity(self, life_activity_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given life activity

        Args:
            life_activity_id (int | str): identity of life activity
            depth: (int): specifies how many related entities will be traversed to create the response

        Returns:
            Result of request as life activity object
        """
        get_response = self.graph_api_service.get_node(life_activity_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=life_activity_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Life_Activity":
            return NotFoundByIdModel(id=life_activity_id, errors="Node not found.")

        life_activity = create_stub_from_response(get_response, properties=['life_activity'])

        if depth != 0:
            life_activity["observable_informations"] = []

            relations_response = self.graph_api_service.get_node_relationships(life_activity_id)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == life_activity_id & relation["name"] == "hasLifeActivity":
                    life_activity['observable_informations'].append(
                        self.observable_information_service.
                        get_observable_information(relation["start_node"], depth - 1))

            return LifeActivityOut(**life_activity)
        else:
            return BasicLifeActivityOut(**life_activity)
