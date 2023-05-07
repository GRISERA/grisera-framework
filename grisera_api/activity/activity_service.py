from activity.activity_model import ActivityIn


class ActivityService:
    """
    Abstract class to handle logic of activity requests

    """

    def save_activity(self, activity: ActivityIn):
        """
        Send request to graph api to create new activity

        Args:
            activity (ActivityIn): Activity to be added

        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def get_activities(self):
        """
        Send request to graph api to get all activities

        Returns:
            Result of request as list of activity objects
        """
        raise Exception("Reference to an abstract class.")

    def get_activity(self, activity_id: int):
        """
        Send request to graph api to get given activity
        Args:
            activity_id (int): Id of activity
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def delete_activity(self, activity_id: int):
        """
        Send request to graph api to get given activity
        Args:
            activity_id (int): Id of activity
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")

    def update_activity(self, activity_id: int, activity: ActivityIn):
        """
        Send request to graph api to update given activity
        Args:
            activity_id (int): Id of activity
            activity (ActivityIn): Activity to be updated
        Returns:
            Result of request as activity object
        """
        raise Exception("Reference to an abstract class.")
