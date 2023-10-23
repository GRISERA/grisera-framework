from typing import Union
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut, ActivityExecutionPropertyIn, ActivityExecutionRelationIn
from activity.activity_service_relational import ActivityServiceRelational
from arrangement.arrangement_service_relational import ArrangementServiceRelational
from rdb_api_service import RdbApiService
from models.not_found_model import NotFoundByIdModel


class ActivityExecutionServiceRelational(ActivityExecutionService):
    
    rdb_api_service = RdbApiService()
    activity_service = ActivityServiceRelational()
    arrangement_service = ArrangementServiceRelational()
    table_name = "Activity_Execution"

    def save_activity_execution(self, activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to create new activity execution

        Args:
            activity_execution (ActivityExecutionIn): Activity execution to be added

        Returns:
            Result of request as activity execution object
        """

        related_activity = self.activity_service.get_activity(activity_execution.activity_id)
        if type(related_activity) is NotFoundByIdModel:
            return ActivityExecutionOut(errors="Activity not found")
        
        related_arrangement = self.arrangement_service.get_arrangement(activity_execution.arrangement_id)
        if type(related_arrangement) is NotFoundByIdModel:
            return ActivityExecutionOut(errors="Arrangement not found")

        activity_exec_data = {
            "activity_id": activity_execution.activity_id,
            "arrangement_id": activity_execution.arrangement_id,
            "additional_properties": activity_execution.additional_properties
        }

        saved_activity_exec = self.rdb_api_service.post(self.table_name, activity_exec_data)

        return ActivityExecutionOut(id=saved_activity_exec["id"], 
                                    activity_id=saved_activity_exec["activity_id"],
                                    arrangement_id=saved_activity_exec["arrangement_id"],
                                    additional_properties=saved_activity_exec["additional_properties"])

    def get_activity_executions(self):
        """
        Send request to graph api to get activity executions

        Returns:
            Result of request as list of activity executions objects
        """

        raise Exception("Reference to an abstract class.")

    def get_activity_execution(self, activity_execution_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given activity execution

        Args:
            depth (int): specifies how many related entities will be traversed to create the response
            activity_execution_id (int | str): identity of activity execution

        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def delete_activity_execution(self, activity_execution_id: Union[int, str]):
        """
        Send request to graph api to delete given activity execution
        Args:
            activity_execution_id (int | str): identity of activity execution
        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity_execution(self, activity_execution_id: Union[int, str],
                                  activity_execution: ActivityExecutionPropertyIn):
        """
        Send request to graph api to update given participant state
        Args:
            activity_execution_id (int | str): identity of activity execution
            activity_execution (ActivityExecutionPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity_execution_relationships(self, activity_execution_id: Union[int, str],
                                                activity_execution: ActivityExecutionRelationIn):
        """
        Send request to graph api to update given activity execution relationships
        Args:
            activity_execution_id (int | str): identity of activity execution
            activity_execution (ActivityExecutionIn): Relationships to update
        Returns:
            Result of request as activity execution object
        """
        raise Exception("Reference to an abstract class.")