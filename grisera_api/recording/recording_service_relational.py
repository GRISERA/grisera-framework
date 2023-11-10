import json
from typing import Union
from models.not_found_model import NotFoundByIdModel
from recording.recording_model import RecordingIn, RecordingOut, RecordingPropertyIn, RecordingRelationIn, RecordingsOut
from rdb_api_service import RdbApiService, Collections
from recording.recording_service import RecordingService


class RecordingServiceRelational(RecordingService):
    
    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.RECORDING


    def save_recording(self, recording: RecordingIn):
        recording_data = {
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in recording.additional_properties
            ])
        }
        result = self.rdb_api_service.post(self.table_name, recording_data)
        if result["errors"] is not None:
                return RecordingOut(errors=result["errors"])
        return RecordingOut(**result["records"])


    def get_recordings(self):
        results = self.rdb_api_service.get(self.table_name)
        return RecordingsOut(recordings=results)


    def get_recording(self, recording_id: Union[int, str], depth: int = 0, source: str = ""):
        import registered_channel.registered_channel_service_relational as rc_rel
        registered_channel_service = rc_rel.RegisteredChannelServiceRelational()

        #import participation.participation_service_relational as p_rel
        #participation_service = p_rel.ParticipationServiceRelational()

        import observable_information.observable_information_service_relational as oi_rel
        observable_information_service = oi_rel.ObservableInformationServiceRelational()

        recording_dict = self.rdb_api_service.get_with_id(self.table_name, recording_id)
        if not recording_dict:
            return NotFoundByIdModel(id=recording_id, errors={"Entity not found."})
        
        if depth > 0:
            if source != Collections.REGISTERED_CHANNEL:
                recording_dict["registered_channel"] = registered_channel_service.get_registered_channel(recording_dict["registered_channel_id"], depth - 1, self.table_name)
            # TODO if source != Collections.PARTICIPATION:
            #    recording_dict["participation"] = participation_service.get_participation(recording_dict["participation_id"], depth - 1, self.table_name)
            if source != Collections.OBSERVABLE_INFORMATION:
                recording_dict["observable_informations"] = observable_information_service.get_multiple_with_foreign_id(recording_id, depth - 1, self.table_name)
        return RecordingOut(**recording_dict)
    

    def delete_recording(self, recording_id: Union[int, str]):
        result = self.get_recording(recording_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, recording_id)
        return result


    def update_recording(self, recording_id: Union[int, str], recording: RecordingPropertyIn):
        recording_data = {
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in recording.additional_properties
            ])
        }
        result = self.get_recording(recording_id)
        if type(result) != NotFoundByIdModel:
            put_result = self.rdb_api_service.put(self.table_name, recording_id, recording_data)
            if put_result["errors"] is not None:
                    return RecordingOut(errors = put_result["errors"])
            return RecordingOut(**put_result["records"])
        return result
    

    def update_recording_relationships(self, recording_id: Union[int, str],
                                       recording: RecordingRelationIn):
        result = self.get_recording(recording_id)
        if type(result) != NotFoundByIdModel:
            put_result = self.rdb_api_service.put(self.table_name, recording_id, recording.dict())
            if put_result["errors"] is not None:
                return RecordingOut(errors = put_result["errors"])
            return RecordingOut(**put_result["records"])
        return result


    def get_multiple_with_foreign_id(self, foreign_id: Union[int, str], depth: int = 0, source: str = ""):
        import registered_channel.registered_channel_service_relational as rc_rel
        registered_channel_service = rc_rel.RegisteredChannelServiceRelational()

        #import participation.participation_service_relational as p_rel
        #participation_service = p_rel.ParticipationServiceRelational()

        import observable_information.observable_information_service_relational as oi_rel
        observable_information_service = oi_rel.ObservableInformationServiceRelational()
        
        response = self.rdb_api_service.get_records_with_foreign_id(self.table_name, source + "_id", foreign_id)
        if response["errors"] is not None:
            return []
        
        recordings = response["records"]
        if depth > 0:
            for recording in recordings:
                if source != Collections.REGISTERED_CHANNEL:
                    recording["registered_channel"] = registered_channel_service.get_registered_channel(recording["registered_channel_id"], depth - 1, self.table_name)
                # TODO if source != Collections.PARTICIPATION:
                    #recording["participation"] = participation_service.get_participation(recording["participation_id"], depth - 1, self.table_name)
                if source != Collections.OBSERVABLE_INFORMATION:
                    recording["observable_informations"] = observable_information_service.get_multiple_with_foreign_id(recording["id"], depth - 1, self.table_name)
        return recordings

