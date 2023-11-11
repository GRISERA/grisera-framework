from typing import Union
from models.not_found_model import NotFoundByIdModel
from participation.participation_model import ParticipationIn, ParticipationOut, ParticipationsOut
from rdb_api_service import RdbApiService, Collections
from participation.participation_service import ParticipationService


class ParticipationServiceRelational(ParticipationService):
    
    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.PARTICIPATION


    def save_participation(self, participation: ParticipationIn):
        result = self.rdb_api_service.post(self.table_name, participation.dict())["records"]
        if result["errors"] is not None:
            return ParticipationOut(errors=result["errors"])
        return ParticipationOut(**result)


    def get_participations(self):
        results = self.rdb_api_service.get(self.table_name)
        return ParticipationsOut(participations=results)


    def get_participation(self, participation_id: Union[int, str], depth: int = 0, source: str = ""):
        import recording.recording_service_relational as rec_rel
        #import activity_execution.activity_execution_service_relational as ae_rel
        #import participant_state.participant_state_service_relational as ps_rel
        recording_service = rec_rel.RecordingServiceRelational() 
        #activity_execution_service = ae_rel.ActivityExecutionServiceRelational()
        #participant_state_service = ps_rel.ParticipantStateServiceRelational()
        
        participation_dict = self.rdb_api_service.get_with_id(self.table_name, participation_id)
        if not participation_dict:
            return NotFoundByIdModel(id=participation_id, errors={"Entity not found."})
        
        if depth > 0:
            if source != Collections.RECORDING:
                participation_dict["recordings"] = recording_service.get_multiple_with_foreign_id(participation_id, depth - 1, self.table_name)
            # TODO if source != Collections.ACTIVITY_EXECUTION:
            #    participation_dict["activity_execution"] = activity_execution_service.get_activity_execution(participation_dict["activity_execution_id"], depth - 1, self.table_name)
            # TODO if source != Collections.PARTICIPANT_STATE:
            #    participation_dict["participant_state"] = participant_state_service.get_participant_state(participation_dict["participant_state_id"], depth - 1, self.table_name)
        
        return ParticipationOut(**participation_dict)


    def delete_participation(self, participation_id: Union[int, str]):
        result = self.get_participation(participation_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, participation_id)
        return result


    def update_participation_relationships(self, participation_id: Union[int, str],
                                           participation: ParticipationIn):
        result = self.get_participation(participation_id)
        if type(result) == NotFoundByIdModel:
            return result
        
        put_result = self.rdb_api_service.put(self.table_name, participation_id, participation.dict())
        if put_result["errors"] is not None:
            return ParticipationOut(errors = put_result["errors"])
        return ParticipationOut(**put_result["records"])


    def get_multiple_with_foreign_id(self, id: Union[int, str], depth: int = 0, source: str = ""):
        import recording.recording_service_relational as rec_rel
        #import activity_execution.activity_execution_service_relational as ae_rel
        #import participant_state.participant_state_service_relational as ps_rel
        recording_service = rec_rel.RecordingServiceRelational() 
        #activity_execution_service = ae_rel.ActivityExecutionServiceRelational()
        #participant_state_service = ps_rel.ParticipantStateServiceRelational()

        participation_dict_list = self.rdb_api_service.get_records_with_foreign_id(self.table_name, source + "_id", id)
        if participation_dict_list["errors"] is not None:
            return []
        if depth <= 0:
            return participation_dict_list["records"]
        
        for participation_dict in participation_dict_list:
            if source != Collections.RECORDING:
                participation_dict["recordings"] = recording_service.get_multiple_with_foreign_id(participation_id, depth - 1, self.table_name)
            # TODO if source != Collections.ACTIVITY_EXECUTION:
            #    participation_dict["activity_execution"] = activity_execution_service.get_activity_execution(participation_dict["activity_execution_id"], depth - 1, self.table_name)
            # TODO if source != Collections.PARTICIPANT_STATE:
            #    participation_dict["participant_state"] = participant_state_service.get_participant_state(participation_dict["participant_state_id"], depth - 1, self.table_name)
        
        return participation_dict_list["records"]
    
