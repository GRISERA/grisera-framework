import json
from typing import Union
from activity.activity_model import ActivityIn, ActivityOut,  ActivitiesOut
from activity.activity_service import ActivityService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections


class ActivityServiceRelational(ActivityService):

    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.ACTIVITY


    def save_activity(self, activity: ActivityIn):
        activity_dict = {
            "activity_name": activity.activity_name,
            "activity": activity.activity,
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in activity.additional_properties
            ])
        }
        
        saved_activity_dict = self.rdb_api_service.post(self.table_name, activity_dict)["records"]
        return ActivityOut(**saved_activity_dict)


    def get_activities(self):
        results = self.rdb_api_service.get(self.table_name)
        return ActivitiesOut(activities=results)


    def get_activity(self, activity_id: Union[int, str], depth: int = 0, source: str = ""):
        #import activity_execution.activity_execution_service as ae_rel
        #activity_execution_service = ae_rel.ActivityExecutionService()
        
        activity_dict = self.rdb_api_service.get_with_id(self.table_name, activity_id)
        if not activity_dict:
            return NotFoundByIdModel(id=activity_id, errors={"Entity not found."})
        
        if depth > 0 and source != Collections.ACTIVITY_EXECUTION:
            #activity_dict["activity_executions"] = activity_execution_service.get_multiple_with_foreign_id(activity_id, depth - 1, self.table_name)
            pass

        return ActivityOut(**activity_dict)

