from typing import Union

import channel.channel_service_relational
import recording.recording_service_relational
import registered_data.registered_data_service_relational
from models.not_found_model import NotFoundByIdModel
from registered_channel.registered_channel_model import RegisteredChannelIn, RegisteredChannelOut, RegisteredChannelsOut
from registered_channel.registered_channel_service import RegisteredChannelService
from rdb_api_service import RdbApiService, Collections


class RegisteredChannelServiceRelational(RegisteredChannelService):
    
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.REGISTERED_CHANNEL


    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        result = self.rdb_api_service.post(self.table_name, registered_channel.dict())
        if result["errors"] is not None:
            return RegisteredChannelOut(errors=result["errors"])
        return RegisteredChannelOut(**result["records"])


    def get_registered_channels(self):
        results = self.rdb_api_service.get(self.table_name)
        return RegisteredChannelsOut(registered_channels=results)


    def get_registered_channel(self, registered_channel_id: Union[int, str], depth: int = 0, source: str = ""):
        registered_channel = self.rdb_api_service.get_with_id(self.table_name, registered_channel_id)
        if not registered_channel:
            return NotFoundByIdModel(id=registered_channel_id, errors={"Entity not found"})
        
        import registered_data.registered_data_service_relational
        registered_data_service_relational = registered_data.registered_data_service_relational.RegisteredDataServiceRelational()

        import recording.recording_service_relational
        recording_service = recording.recording_service_relational.RecordingServiceRelational()

        if depth > 0:
            registered_channel["registeredData"] = registered_data_service_relational.get_registered_data(
                registered_channel["registered_data_id"], depth - 1, self.table_name)
            # registered_channel["channels"] = self.channels_service.get_channel(
            #TODO     registered_channel["channel_id"], depth - 1, self.table_name)
            if source != Collections.RECORDING:
                registered_channel["recordings"] = self.recording_service.get_recording(
                    registered_channel["registered_data_id"], depth - 1, self.table_name)
        return RegisteredChannelOut(**registered_channel)


    def get_multiple_with_foreign_id(self, foreign_id: Union[int, str], depth: int = 0, source: str = ""):
        response = self.rdb_api_service.get_records_with_foreign_id(self.table_name, source+"_id",foreign_id)
        if response["errors"] is not None:
            return []
        registered_channels = response["records"]

        import registered_data.registered_data_service_relational
        registered_data_service_relation = registered_data.registered_data_service_relational.RegisteredDataServiceRelational()

        import recording.recording_service_relational
        recording_service = recording.recording_service_relational.RecordingServiceRelational()

        if depth > 0:
            for registered_channel in registered_channels:
                if source != Collections.REGISTERED_DATA:
                    registered_channel["registeredData"] = registered_data_service_relation.get_registered_data(
                        registered_channel["registered_data_id"], depth - 1, self.table_name)
                # if source != Collections.CHANNEL:
                #TODO     registered_channel["channels"] = self.channels_service.get_channel(
                #         registered_channel["channel_id"], depth - 1, self.table_name)
                if source != Collections.RECORDING:
                    registered_channel["recordings"] = recording_service.get_multiple_with_foreign_id(registered_channel["registered_data_id"], depth - 1, self.table_name)
        return registered_channels


    def update_registered_channel_relationships(self, registered_channel_id: Union[int, str],
                                                registered_channel: RegisteredChannelIn):
        result = self.get_registered_channel(registered_channel_id)
        if type(result) != NotFoundByIdModel:
            put_result = self.rdb_api_service.put(self.table_name, registered_channel_id, registered_channel.dict())
            if put_result["errors"] is not None:
                return RegisteredChannelOut(errors=put_result["errors"])
            return RegisteredChannelOut(**put_result["records"])
        return result


    def delete_registered_channel(self, registered_channel_id: Union[int, str]):
        result = self.get_registered_data(registered_channel_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, registered_channel_id)
        return result

