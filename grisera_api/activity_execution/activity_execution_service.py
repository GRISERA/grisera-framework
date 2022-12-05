from activity_execution.activity_execution_model import ActivityExecutionPropertyIn, ActivityExecutionRelationIn, \
    ActivityExecutionIn, ActivityExecutionOut, ActivityExecutionsOut, BasicActivityExecutionOut
from arrangement.arrangement_service import ArrangementService
from graph_api_service import GraphApiService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ActivityExecutionService:
    """
    Abstract class to handle logic of activities requests

    """

    def save_activity_execution(self, activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to create new activity execution

        Args:
            activity_execution (ActivityExecutionIn): Activity execution to be added

        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def get_activity_executions(self):
        """
        Send request to graph api to get activity executions

        Returns:
            Result of request as list of activity executions objects
        """

        raise Exception("Reference to an abstract class.")

    def get_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to get given activity execution

        Args:
            activity_execution_id (int): Id of activity execution

        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def delete_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to delete given activity execution
        Args:
            activity_execution_id (int): Id of activity execution
        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity_execution(self, activity_execution_id: int, activity_execution: ActivityExecutionPropertyIn):
        """
        Send request to graph api to update given participant state
        Args:
            activity_execution_id (int): Id of participant state
            activity_execution (ActivityExecutionPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity_execution_relationships(self, activity_execution_id: int,
                                                activity_execution: ActivityExecutionRelationIn):
        """
        Send request to graph api to update given activity execution relationships
        Args:
            activity_execution_id (int): Id of activity execution
            activity_execution (ActivityExecutionIn): Relationships to update
        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")
