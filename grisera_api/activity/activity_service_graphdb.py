from typing import Union

from activity_execution.activity_execution_service import ActivityExecutionService
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
        self.activity_execution_service: ActivityExecutionService = None

    def save_activity(self, activity: ActivityIn,dataset_name: str):

        """
        Send request to graph api to create new activity

        Args:
            activity (ActivityIn): Activity to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as activity object
        """

        node_response = self.graph_api_service.create_node("Activity", dataset_name)

        if node_response["errors"] is not None:
            return ActivityOut(activity=activity.activity, errors=node_response["errors"])

        activity_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(activity_id, activity, dataset_name)
        if properties_response["errors"] is not None:
            return ActivityOut(activity=activity.activity, errors=properties_response["errors"])

        return ActivityOut(activity=activity.activity, id=activity_id)

    def get_activities(self, dataset_name: str):
        """
        Send request to graph api to get all activities

        Args:
            dataset_name (str): name of dataset
        Returns:
            Result of request as list of activity objects
        """
        get_response = self.graph_api_service.get_nodes("Activity", dataset_name)
        if get_response["errors"] is not None:
            return ActivitiesOut(errors=get_response["errors"])
        activities = [BasicActivityOut(id=activity["id"], activity=activity["properties"][0]["value"])
                      for activity in get_response["nodes"]]

        return ActivitiesOut(activities=activities)


    def get_activity(self, activity_id: Union[int, str],dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given activity
        Args:
            activity_id (int | str): identity of activity
            dataset_name (str): name of dataset
            depth(int): specifies how many related entities will be traversed to create the response

        Returns:
            Result of request as activity object
        """
        get_response = self.graph_api_service.get_node(activity_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=activity_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Activity":
            return NotFoundByIdModel(id=activity_id, errors="Node not found.")

        activity = create_stub_from_response(get_response, properties=['activity'])

        if depth != 0:
            activity['activity_executions'] = []
            relations_response = self.graph_api_service.get_node_relationships(activity_id, dataset_name)


            for relation in relations_response["relationships"]:
                if relation["end_node"] == str(activity_id) and relation["name"] == "hasActivity":
                    activity['activity_executions']. \
                        append(
                        self.activity_execution_service.get_activity_execution(relation["start_node"], depth - 1))

            return ActivityOut(**activity)
        else:
            return BasicActivityOut(**activity)

    def delete_activity(self, activity_id: int, dataset_name: str):
        """
        Send request to graph api to get given activity
        Args:
            activity_id (int): Id of activity
            dataset_name (str): name of dataset
        Returns:
            Result of request as activity object
        """
        get_response = self.get_activity(activity_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(activity_id, dataset_name)
        return get_response

    def update_activity(self, activity_id: int, activity: ActivityIn, dataset_name: str):
        """
        Send request to graph api to update given activity
        Args:
            activity_id (int): Id of activity
            activity (ActivityIn): Activity to be updated
            dataset_name (str): name of dataset

        Returns:
            Result of request as activity object
        """
        get_response = self.get_activity(activity_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        self.graph_api_service.delete_node_properties(activity_id, dataset_name)
        self.graph_api_service.create_properties(activity_id, activity, dataset_name)

        activity_result = {'id': activity_id, 'relations': get_response.relations,
                             'reversed_relations': get_response.reversed_relations}
        activity_result.update(get_response.dict())

        return ActivityOut(**activity_result)

