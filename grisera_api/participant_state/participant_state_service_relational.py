from typing import Union
from participant_state.participant_state_model import ParticipantStateOut, BasicParticipantStateOut
from models.not_found_model import NotFoundByIdModel
from participant_state.participant_state_service import ParticipantStateService
from rdb_api_service import RdbApiService


class ParticipantStateServiceRelational(ParticipantStateService):

    rdb_api_service = RdbApiService()
    table_name = "participant_state"

    def get_participant_state(self, participant_state_id: Union[int, str], depth: int = 0):
        participant_state = self.rdb_api_service.get_with_id(self.table_name, participant_state_id)

        if not participant_state:
            return NotFoundByIdModel(id=participant_state_id, errors="Entity not found.")
        
        return ParticipantStateOut(id=participant_state["id"])
    
    def get_multiple_with_foreign_id(self, id: Union[int, str], depth: int = 0, source: str = ""):
        participant_states_dict = self.rdb_api_service.get_records_with_foreign_id(self.table_name, "{}_id".format(source), id)
        return participant_states_dict
