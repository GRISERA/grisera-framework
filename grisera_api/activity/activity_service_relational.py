from typing import Union
from activity.activity_model import ActivityOut, BasicActivityOut, ActivitiesOut
from activity.activity_service import ActivityService
from property.property_model import PropertyIn
from rdb_api_service import RdbApiService


class ActivityServiceRelational(ActivityService):

    rdb_api_service = RdbApiService()
    table_name = "Activity"

    def get_activities(self):
        results = self.rdb_api_service.get(self.table_name)
        activities = []
        for activity in results:
            additional_properties = []
            for k, v in activity["additional_properties"].items():
                additional_properties.append(PropertyIn(key=k, value=v))
            activities.append(BasicActivityOut(id=activity["id"], activity=activity["activity"], additional_properties=additional_properties))    

        return ActivitiesOut(activities=activities)

    def get_activity(self, activity_id: int | str, depth: int = 0):
        activity = self.rdb_api_service.get_with_id(self.table_name, activity_id)
        additional_properties = []
        for k, v in activity["additional_properties"].items():
            additional_properties.append(PropertyIn(key=k, value=v))

        return ActivityOut(id=activity["id"], activity=activity["activity"], additional_properties=additional_properties)
