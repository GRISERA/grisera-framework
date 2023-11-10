import json
from typing import Union
from models.not_found_model import NotFoundByIdModel
from participant.participant_model import ParticipantIn, ParticipantOut, ParticipantsOut
from participant.participant_service import ParticipantService
from rdb_api_service import RdbApiService, Collections


class ParticipantServiceRelational(ParticipantService):
    

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.PARTICIPANT

    def save_participant(self, participant: ParticipantIn):
        participant_data_dict = {
            "name": participant.name,
            "date_of_birth": participant.date_of_birth,
            "sex": participant.sex,
            "disorder": participant.disorder,
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in participant.additional_properties
            ])
        }
        saved_participant_dict = self.rdb_api_service.post(self.table_name, participant_data_dict)["records"]
        return ParticipantOut(**saved_participant_dict)

    def get_participants(self):
        results = self.rdb_api_service.get(self.table_name)
        return ParticipantsOut(participants=results)
    
    def get_participant(self, participant_id: Union[int, str], depth: int = 0, source: str = ""):
        participant_dict = self.rdb_api_service.get_with_id(self.table_name, participant_id)
        if not participant_dict:
            return NotFoundByIdModel(id=participant_id, errors={"Entity not found"})
        
        # import participant_state.participant_state_service_relational
        # participant_state_service = participant_state.participant_state_service_relational.ParticipantStateServiceRelational()
        # if depth > 0:
        #     if source != Collections.PARTICIPANT_STATE:
        #         participant_dict["participant_states"] = participant_state_service.get_multiple_with_foreign_id(participant_id, depth - 1, self.table_name)

        return ParticipantOut(**participant_dict)
    
    def delete_participant(self, participant_id: Union[int, str]):
        result = self.get_participant(participant_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, participant_id)
        return result
    
    def update_participant(self, participant_id: Union[int, str], participant: ParticipantIn):
        participant_data_dict = {
            "name": participant.name,
            "date_of_birth": participant.date_of_birth,
            "sex": participant.sex,
            "disorder": participant.disorder,
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in participant.additional_properties
            ])
        }

        result = self.get_participant(participant_id)
        if type(result) == NotFoundByIdModel:
            return result
        
        put_result = self.rdb_api_service.put(self.table_name, participant_id, participant_data_dict)
        if put_result["errors"] is not None:
            return ParticipantOut(errors = put_result["errors"])
        return ParticipantOut(**put_result["records"])

            