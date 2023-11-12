from typing import Union
from models.not_found_model import NotFoundByIdModel
from life_activity.life_activity_model import LifeActivitiesOut, LifeActivityIn, LifeActivityOut
from rdb_api_service import RdbApiService, Collections
from life_activity.life_activity_service import LifeActivityService


class LifeActivityServiceRelational(LifeActivityService):
    
    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.LIFE_ACTIVITY


    def get_life_activities(self):
        results = self.rdb_api_service.get(self.table_name)
        return LifeActivitiesOut(life_activities=results)


    def get_life_activity(self, life_activity_id: Union[int, str], depth: int = 0, source: str = ""):
        import observable_information.observable_information_service_relational as oi_rel
        observable_information_service = oi_rel.ObservableInformationServiceRelational()
        
        life_activity_dict = self.rdb_api_service.get_with_id(self.table_name, life_activity_id)
        if not life_activity_dict:
            return NotFoundByIdModel(id=life_activity_dict, errors={"Entity not found."})
        if depth > 0 and source != Collections.OBSERVABLE_INFORMATION:
            life_activity_dict["observable_informations"] = observable_information_service.get_multiple_with_foreign_id(life_activity_id, depth - 1, self.table_name)
        return LifeActivityOut(**life_activity_dict)
    
