from channel.channel_service import ChannelService
from channel.channel_model import ChannelIn, Type
import os
from time import sleep


class SetupNodes:
    """
    Class to init nodes in grahp database
    """
    def set_channels(self):
        """
        Initialize values of channels
        """
        channel_service = ChannelService()

        if not os.path.exists("lock"):
            open("lock", "w").write("Busy")
            sleep(30)
            created_types = [channel.type for channel in channel_service.get_channels().channels]

            [channel_service.save_channel(ChannelIn(type=channel_type.value)) for channel_type in Type
             if channel_type.value not in created_types]
            os.remove("lock")
