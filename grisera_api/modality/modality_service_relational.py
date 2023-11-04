from typing import Union
from models.not_found_model import NotFoundByIdModel
from modality.modality_model import ModalityIn, Modality, ModalitiesOut, ModalityOut
from rdb_api_service import RdbApiService
from modality.modality_service import ModalityService


class ModalityServiceRelational(ModalityService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = "modality"

    def save_modality(self, modality: ModalityIn):
        if not self.is_valid_modality(modality):
            return ModalityOut(modality=modality.modality, errors="Invalid modality type")
        
        modality_data = {
            "modality": modality.modality
        }
        saved_modality_dict = self.rdb_api_service.post(self.table_name, modality_data)
        return ModalityOut(**saved_modality_dict)

    def get_modalities(self):
        results = self.rdb_api_service.get(self.table_name)
        return ModalitiesOut(modalities=results)

    def get_modality(self, modality_id: Union[int, str], depth: int = 0):
        result = self.rdb_api_service.get_with_id(self.table_name, modality_id)
        if not result:
            return NotFoundByIdModel(id=modality_id, errors={"Entity not found."})
        return ModalityOut(**result)

    def is_valid_modality(self, modality: ModalityIn):
        valid_modalities = [Modality.facial_expressions, Modality.body_posture, Modality.eye_gaze, \
                            Modality.head_movement, Modality.gestures, Modality.motion, \
                            Modality.prosody_of_speech, Modality.vocalization, Modality.heart_rate, \
                            Modality.hrv, Modality.muscle_tension, Modality.skin_conductance, \
                            Modality.resp_intensity_and_period, Modality.peripheral_temperature, \
                            Modality.neural_activity]
        
        return modality.modality in valid_modalities
    