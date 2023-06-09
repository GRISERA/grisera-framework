from typing import Union


from activity.activity_model import ActivityIn, ActivityOut, Activity
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
        Send request to ontology api to create new activity

        Args:
            activity (ActivityIn): Activity to be added

        Returns:
            Result of request as activity object
        """
        model_id = 1
        class_name = ""
        if activity.activity == Activity.individual:
            class_name = "IndividualActivity"
        elif activity.activity == Activity.group:
            class_name = "GroupActivity"
        elif activity.activity == Activity.two_people:
            class_name = "TwoPersonsActivity"
        else:
            return ActivityOut(**activity.dict(), errors=f"Wrong type of activity: {activity.activity}")

        instance_response_activity = self.ontology_api_service.add_instance(model_id, class_name,
                                                                            activity.activity_name)
        if instance_response_activity["errors"] is not None:
            return ActivityOut(**activity.dict(), errors=instance_response_activity["errors"])

        new_additional_properties = []

        errors = None

        for prop in activity.additional_properties:
            response = self.ontology_api_service.add_role(model_id, prop.key, activity.activity_name, prop.value)
            if response["errors"] is not None:
                errors = f"[{prop.key} : {prop.value}]:" + response["errors"]
                break
            else:
                new_additional_properties.append(prop)

        experiment_label = instance_response_activity["label"]
        activity.__dict__.update({'experiment_name': experiment_label})
        activity.__dict__.update({'additional_properties': new_additional_properties})

        if errors is None:
            return ActivityOut(**activity.dict())
        else:
            return ActivityOut(**activity.dict(), errors=errors)


    def get_activities(self):
        super().get_activities()

    def get_activity(self, activity_id: Union[int, str], depth: int = 0):
        super().get_activity(activity_id, depth)

