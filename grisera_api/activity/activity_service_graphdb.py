from graph_api_service import GraphApiService
from activity.activity_model import ActivityIn, ActivityOut, ActivitiesOut, BasicActivityOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ActivityServiceGraphDB:
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

    def get_activity(self, activity_id: int):
        """
        Send request to graph api to get given activity
        Args:
            activity_id (int): Id of activity
        Returns:
            Result of request as activity object
        """
        get_response = self.graph_api_service.get_node(activity_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=activity_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Activity":
            return NotFoundByIdModel(id=activity_id, errors="Node not found.")

        activity = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            activity[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(activity_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == activity_id:
                activity['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                 name=relation["name"], relation_id=relation["id"]))
            else:
                activity['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                          name=relation["name"],
                                                                          relation_id=relation["id"]))

        return ActivityOut(**activity)
