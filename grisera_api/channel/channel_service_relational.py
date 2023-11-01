from typing import Union
from channel.channel_service import ChannelService
from channel.channel_model import ChannelIn, ChannelOut, ChannelsOut
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService
from registered_channel.registered_channel_service import RegisteredChannelService

class ChannelServiceRelational(ChannelService):
    rdb_api_service = RdbApiService()
    table_name = "channel"

    def __init__(self):
        self.registered_channel_service = RegisteredChannelService()

    def get_channels(self):
        results = self.rdb_api_service.get(self.table_name)
        return  ChannelsOut(channels=results)
    
    def get_channel(self, channel_id: Union[int, str], depth: int = 0, source: str = ""):
        channel_dict = self.rdb_api_service.get_with_id(self.table_name, channel_id)
        if not channel_dict:
            return NotFoundByIdModel(id=channel_id, errors={"Entity not found."})
        
        if depth > 0:
            if source != "registered_channel":
                # not implemented yet
                channel_dict["registered_channels"] = self.registered_channel_service.get_single_with_foreign_id(channel_id, depth - 1, self.table_name)

        return ChannelOut(**channel_dict)
