from grisera_api.activity.activity_model import BasicActivityOut, ActivitiesOut
from grisera_api.activity.activity_service import ActivityService
from grisera_api.rdb_api_service import RdbApiService



class ActivityServiceRelational(ActivityService):
    rdb_api_service = RdbApiService()
    table_name = "Activity"
    def get_activities(self):
        results = self.rdb_api_service.get(self.table_name)
        activities = [BasicActivityOut(id=activity["id"], activity=activity["activity"],
        additional_properties=activity["additional_properties"]) for activity in results]
        return ActivitiesOut(activities)


