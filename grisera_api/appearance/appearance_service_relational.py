from typing import Union
from appearance.appearance_model import AppearancesOut, BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut, AppearanceOcclusionOut, AppearanceSomatotypeOut, AppearanceOcclusionIn, AppearanceSomatotypeIn
from models.not_found_model import NotFoundByIdModel
from appearance.appearance_service import AppearanceService
from rdb_api_service import RdbApiService
from participant_state.participant_state_service_relational import ParticipantStateServiceRelational


class AppearanceServiceRelational(AppearanceService):

    rdb_api_service = RdbApiService()
    table_name = "appearance"

    def __init__(self):
        self.participant_state_service = ParticipantStateServiceRelational()

    def save_appearance_occlusion(self, appearance: AppearanceOcclusionIn):
        appearance_data = {
            "type": "occlusion",
            "beard": appearance.beard,
            "moustache": appearance.moustache,
            "glasses": appearance.glasses
        }

        saved_appearance_dict = self.rdb_api_service.post(self.table_name, appearance_data)

        return AppearanceOcclusionOut(**saved_appearance_dict)
    
    def save_appearance_somatotype(self, appearance: AppearanceSomatotypeIn):
        if not self.is_valid_somatotype(appearance):
            return AppearanceSomatotypeOut(ectomorph=appearance.ectomorph, endomorph=appearance.endomorph, 
                                           mesomorph=appearance.mesomorph, errors="Value of one of the parameters is not in range <1, 7>.")   

        appearance_data = {
            "type": "somatotype",
            "ectomorph": appearance.ectomorph,
            "endomorph": appearance.endomorph,
            "mesomorph": appearance.mesomorph
        }

        saved_appearance_dict = self.rdb_api_service.post(self.table_name, appearance_data)

        return AppearanceSomatotypeOut(**saved_appearance_dict)

    def get_appearance(self, appearance_id: Union[int, str], depth: int = 0, source: str = ""):
        appearance_dict = self.rdb_api_service.get_with_id(self.table_name, appearance_id)
        if not appearance_dict:
            return NotFoundByIdModel(id=appearance_id, errors={"Entity not found."})
        
        if depth > 0:
            if source != "participant_state":
                appearance_dict["participant_states"] = self.participant_state_service.get_multiple_with_foreign_id(appearance_id, depth - 1, self.table_name)
        print(appearance_dict)
        return AppearanceOcclusionOut(**appearance_dict) if appearance_dict["type"] == "occlusion" else AppearanceSomatotypeOut(**appearance_dict)
    
    def get_appearances(self):
        results = self.rdb_api_service.get(self.table_name)
        
        appearances = []
        for appearance_dict in results:
            appearances.append(AppearanceOcclusionOut(**appearance_dict) if appearance_dict["type"] == "occlusion" else AppearanceSomatotypeOut(**appearance_dict))
        return  AppearancesOut(appearances=appearances)
    
    def update_appearance_occlusion(self, appearance_id: Union[int, str], appearance: AppearanceOcclusionIn):
        get_response = self.get_appearance(appearance_id)
        if type(get_response) is AppearanceSomatotypeOut:
            return NotFoundByIdModel(id=appearance_id, errors="Entity not found.")
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.put(self.table_name, appearance_id, appearance.dict())
        return self.get_appearance(appearance_id)
    
    def update_appearance_somatotype(self, appearance_id: Union[int, str], appearance: AppearanceSomatotypeIn):
        if not self.is_valid_somatotype(appearance):
            return AppearanceSomatotypeOut(**appearance.dict(), errors="Value of one of the parameters is not in range <1, 7>.")   
        
        get_response = self.get_appearance(appearance_id)
        if type(get_response) is AppearanceOcclusionOut:
            return NotFoundByIdModel(id=appearance_id, errors="Entity not found.")
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.put(self.table_name, appearance_id, appearance.dict())
        return self.get_appearance(appearance_id)

    def delete_appearance(self, appearance_id: Union[int, str]):
        get_response = self.get_appearance(appearance_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, appearance_id)
        return get_response
    
    def is_valid_somatotype(self, appearance):
        return not (appearance.ectomorph < 1 or appearance.ectomorph > 7 \
                or appearance.endomorph < 1 or appearance.endomorph > 7 \
                or appearance.mesomorph < 1 or appearance.mesomorph > 7)