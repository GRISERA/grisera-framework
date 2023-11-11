from typing import Union
from channel.channel_service import ChannelService
from channel.channel_model import ChannelIn, ChannelOut, ChannelsOut
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from registered_channel.registered_channel_service import RegisteredChannelService

class ChannelServiceRelational(ChannelService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.CHANNEL
        self.registered_channel_service = RegisteredChannelService()


    def save_channel(self, channel: ChannelIn):
        saved_channel_dict = self.rdb_api_service.post(self.table_name, channel.dict())
        if saved_channel_dict["errors"] is not None:
             return ChannelOut(errors=saved_channel_dict["errors"])
        return ChannelOut(**saved_channel_dict["records"])

    def get_channels(self):
        results = self.rdb_api_service.get(self.table_name)
        return  ChannelsOut(channels=results)
    

    def get_channel(self, channel_id: Union[int, str], depth: int = 0, source: str = ""):
        channel_dict = self.rdb_api_service.get_with_id(self.table_name, channel_id)
        if not channel_dict:
            return NotFoundByIdModel(id=channel_id, errors={"Entity not found."})
        
        import registered_channel.registered_channel_service_relational
        registered_channel_service = registered_channel.registered_channel_service_relational.RegisteredChannelServiceRelational()

        if depth > 0 and source != Collections.REGISTERED_CHANNEL:
                channel_dict["registered_channels"] = registered_channel_service.get_multiple_with_foreign_id(channel_id, depth - 1, self.table_name)

        return ChannelOut(**channel_dict)