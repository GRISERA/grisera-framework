import json
from typing import Union
from activity.activity_model import ActivityIn, ActivityOut, BasicActivityOut, ActivitiesOut, Activity
from activity.activity_service import ActivityService
from activity_execution.activity_execution_service import ActivityExecutionService
from models.not_found_model import NotFoundByIdModel
from property.property_model import PropertyIn
from rdb_api_service import RdbApiService, Collections


class ActivityServiceRelational(ActivityService):

    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.activity_execution_service = ActivityExecutionService()
        self.table_name = Collections.ACTIVITY

    def save_activity(self, activity: ActivityIn):
        if not self.is_valid_activity(activity):
            return ActivityOut(activity_name=activity.activity_name, activity=activity.activity, \
                               additional_properties=activity.additional_properties, \
                               errors="Invalid activity type")

        activity_dict = {
            "name": activity.activity_name,
            "activity": activity.activity,
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in activity.additional_properties
            ])
        }
        
        saved_activity_dict = self.rdb_api_service.post(self.table_name, activity_dict)
        return ActivityOut(**saved_activity_dict)

    def get_activity(self, activity_id: Union[int, str], depth: int = 0, source: str = ""):
        activity_dict = self.rdb_api_service.get_with_id(self.table_name, activity_id)
        if not activity_dict:
            return NotFoundByIdModel(id=activity_id, errors={"Entity not found."})
        
        if depth > 0 and source != Collections.ACTIVITY_EXECUTION:
            activity_dict["activity_executions"] = self.activity_execution_service.get_multiple_with_foreign_id(activity_id, depth - 1, self.table_name)

        return ActivityOut(**activity_dict)

    def get_activities(self):
        results = self.rdb_api_service.get(self.table_name)
        return ActivitiesOut(activities=results)

    def is_valid_activity(self, activity: ActivityIn):
        return  activity.activity == Activity.individual or \
                activity.activity == Activity.two_people or  \
                activity.activity == Activity.group
    