from typing import Union

from activity.activity_model import ActivityIn, ActivityOut
from activity.activity_service import ActivityService
from ontology_api_service import OntologyApiService


class ActivityServiceOntology(ActivityService):
    """
    Object to handle logic of activity requests

    Attributes:
    ontology_api_service (OntologyApiService): Service used to communicate with Ontology API
    """
    ontology_api_service = OntologyApiService()

    def save_activity(self, activity: ActivityIn):
        """
        Send request to graph api to create new activity

        Args:
            activity (ActivityIn): Activity to be added

        Returns:
            Result of request as activity object
        """
        model_id = 1
        instance_response_activity = self.ontology_api_service.add_instance(model_id, "Activity", "test")
        if instance_response_activity["errors"] is not None:
            return ActivityOut(**activity.dict(), errors=instance_response_activity["errors"])
        activity_label = instance_response_activity["label"]
        activity.__dict__.update({'activity_name': activity_label})
        return ActivityOut(**activity.dict())

    def get_activities(self):
        super().get_activities()

    def get_activity(self, activity_id: Union[int, str], depth: int = 0):
        super().get_activity(activity_id, depth)

