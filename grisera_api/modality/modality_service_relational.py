from typing import Union

from models.not_found_model import NotFoundByIdModel
from modality.modality_model import ModalityIn, Modality, ModalitiesOut, ModalityOut
from rdb_api_service import RdbApiService, Collections
from modality.modality_service import ModalityService


class ModalityServiceRelational(ModalityService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.observable_information_service = ObservableInformationService()
        self.table_name = Collections.MODALITY

    def save_modality(self, modality: ModalityIn):
        if not self.is_valid_modality(modality):
            return ModalityOut(modality=modality.modality, errors="Invalid modality type")
        
        modality_data = {
            "modality": modality.modality
        }
        result = self.rdb_api_service.post(self.table_name, modality_data)
        if result["errors"] is not None:
            return ModalityOut(errors=result["errors"])
        return ModalityOut(**result["records"])


    def get_modalities(self):
        results = self.rdb_api_service.get(self.table_name)
        return ModalitiesOut(modalities=results)


    def get_modality(self, modality_id: Union[int, str], depth: int = 0, source: str = ""):
        import observable_information.observable_information_service_relational as oi_rel_service
        observable_information_service = oi_rel_service.ObservableInformationServiceRelational()

        result = self.rdb_api_service.get_with_id(self.table_name, modality_id)
        if not result:
            return NotFoundByIdModel(id=modality_id, errors={"Entity not found."})
        
        if depth > 0 and source != Collections.OBSERVABLE_INFORMATION:
            result["observable_informations"] = observable_information_service.get_multiple_with_foreign_id(modality_id, depth - 1, self.table_name)

        return ModalityOut(**result)


    def is_valid_modality(self, modality: ModalityIn):
        valid_modalities = [Modality.facial_expressions, Modality.body_posture, Modality.eye_gaze, \
                            Modality.head_movement, Modality.gestures, Modality.motion, \
                            Modality.prosody_of_speech, Modality.vocalization, Modality.heart_rate, \
                            Modality.hrv, Modality.muscle_tension, Modality.skin_conductance, \
                            Modality.resp_intensity_and_period, Modality.peripheral_temperature, \
                            Modality.neural_activity]
        
        return modality.modality in valid_modalities
    

    def get_single_with_foreign_id(self, modality_id: Union[int, str], depth: int = 0, source: str = ""):
        return self.get_modality(modality_id, depth, source)
    