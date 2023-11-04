from typing import Union
from activity.activity_model import ActivityIn, ActivityOut, BasicActivityOut, ActivitiesOut, Activity
from activity.activity_service import ActivityService
from models.not_found_model import NotFoundByIdModel
from property.property_model import PropertyIn
from rdb_api_service import RdbApiService


class ActivityServiceRelational(ActivityService):

    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = "activity"

    def save_activity(self, activity: ActivityIn):
        if not self.is_valid_activity(activity):
            return ActivityOut(activity_name=activity.activity_name, activity=activity.activity, \
                               additional_properties=activity.additional_properties, \
                               errors="Invalid activity type")

        activity_data = {
            "name": activity.activity_name,
            "activity": activity.activity,
            "additional_properties": activity.additional_properties
        }
        
        saved_activity_dict = self.rdb_api_service.post(self.table_name, activity_data)
        return ActivityOut(**saved_activity_dict)

    def get_activity(self, activity_id: int | str, depth: int = 0):
        activity_dict = self.rdb_api_service.get_with_id(self.table_name, activity_id)
        if not activity_dict:
            return NotFoundByIdModel(id=activity_id, errors={"Entity not found."})
        return ActivityOut(**activity_dict)

    def get_activities(self):
        results = self.rdb_api_service.get(self.table_name)
        return ActivitiesOut(activities=results)

    def is_valid_activity(self, activity: ActivityIn):
        return  activity.activity == Activity.individual or \
                activity.activity == Activity.two_people or  \
                activity.activity == Activity.group
    