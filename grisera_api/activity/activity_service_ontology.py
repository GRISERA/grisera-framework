from typing import Union

from activity.activity_model import ActivityIn
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
        super().save_activity()

    def get_activities(self):
        super().get_activities()

    def get_activity(self, activity_id: Union[int, str], depth: int = 0):
        super().get_activity(activity_id, depth)

