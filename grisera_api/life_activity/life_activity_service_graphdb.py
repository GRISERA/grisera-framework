from graph_api_service import GraphApiService
from life_activity.life_activity_model import LifeActivityIn, LifeActivityOut, LifeActivitiesOut, BasicLifeActivityOut
from life_activity.life_activity_service import LifeActivityService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class LifeActivityServiceGraphDB(LifeActivityService):
    """
    Object to handle logic of life activity requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_life_activity(self, life_activity: LifeActivityIn, database_name: str):
        """
        Send request to graph api to create new life activity

        Args:
            life_activity (LifeActivityIn): Life activity to be added

        Returns:
            Result of request as life activity object
        """

        node_response = self.graph_api_service.create_node("`Life Activity`", database_name)

        if node_response["errors"] is not None:
            return LifeActivityOut(life_activity=life_activity.life_activity, errors=node_response["errors"])

        life_activity_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(life_activity_id, life_activity, database_name)
        if properties_response["errors"] is not None:
            return LifeActivityOut(errors=properties_response["errors"])

        return LifeActivityOut(life_activity=life_activity.life_activity, id=life_activity_id)

    def get_life_activities(self, database_name: str):
        """
        Send request to graph api to get all life activities

        Returns:
            Result of request as list of life activity objects
        """
        get_response = self.graph_api_service.get_nodes("`Life Activity`", database_name)
        if get_response["errors"] is not None:
            return LifeActivitiesOut(errors=get_response["errors"])
        life_activities = [BasicLifeActivityOut(id=life_activity["id"],
                                                life_activity=life_activity["properties"][0]["value"])
                           for life_activity in get_response["nodes"]]

        return LifeActivitiesOut(life_activities=life_activities)

    def get_life_activity(self, life_activity_id: int, database_name: str):
        """
        Send request to graph api to get given life activity

        Args:
        life_activity_id (int): Id of life activity

        Returns:
            Result of request as life activity object
        """
        get_response = self.graph_api_service.get_node(life_activity_id, database_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=life_activity_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Life Activity":
            return NotFoundByIdModel(id=life_activity_id, errors="Node not found.")

        life_activity = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            life_activity[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(life_activity_id, database_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == life_activity_id:
                life_activity['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                      name=relation["name"],
                                                                      relation_id=relation["id"]))
            else:
                life_activity['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                               name=relation["name"],
                                                                               relation_id=relation["id"]))

        return LifeActivityOut(**life_activity)
