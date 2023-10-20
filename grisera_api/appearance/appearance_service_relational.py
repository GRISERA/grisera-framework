from typing import Union
from appearance.appearance_model import AppearancesOut, BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut, AppearanceOcclusionOut, AppearanceSomatotypeOut, AppearanceOcclusionIn
from appearance.appearance_service import AppearanceService
from rdb_api_service import RdbApiService


class AppearanceServiceRelational(AppearanceService):

    rdb_api_service = RdbApiService()
    table_name = "Appearance"

    def get_appearance(self, appearance_id: Union[int, str], depth: int = 0):
        appearance = self.rdb_api_service.get_with_id(self.table_name, appearance_id)

        if appearance["type"] == "somatotype":
            return AppearanceSomatotypeOut(id=appearance["id"], ectomorph=appearance["ectomorph"], endomorph=appearance["endomorph"], 
                                               mesomorph=appearance["mesomorph"])
        elif appearance["type"] == "occlusion":
            return AppearanceOcclusionOut(id=appearance["id"], beard=appearance["beard"], moustache=appearance["moustache"], 
                                               glasses=appearance["glasses"])
    
    def get_appearances(self):
        results = self.rdb_api_service.get(self.table_name)
        appearances = []
        for appearance in results:
            if appearance["type"] == "somatotype":
                appearances.append(BasicAppearanceSomatotypeOut(id=appearance["id"], ectomorph=appearance["ectomorph"], endomorph=appearance["endomorph"], 
                                                                mesomorph=appearance["mesomorph"]))
            elif appearance["type"] == "occlusion":
                appearances.append(BasicAppearanceOcclusionOut(id=appearance["id"], beard=appearance["beard"], moustache=appearance["moustache"], 
                                                                glasses=appearance["glasses"]))
        return  AppearancesOut(appearances=appearances)
    
    def save_appearance_occlusion(self, appearance: AppearanceOcclusionIn):
        appearance_data = {
            "type": "occlusion",
            "beard": appearance.beard,
            "moustache": appearance.moustache,
            "glasses": appearance.glasses
        }

        saved_appearance = self.rdb_api_service.post(self.table_name, appearance_data)

        return AppearanceOcclusionOut(id=saved_appearance["id"], beard=saved_appearance["beard"], moustache=saved_appearance["moustache"], 
                                      glasses=saved_appearance["glasses"])
