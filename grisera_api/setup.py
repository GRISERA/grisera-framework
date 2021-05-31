from channel.channel_service import ChannelService
from channel.channel_model import ChannelIn
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
        channel_types = ["Audio", "BVP", "Chest size", "Depth video", "ECG",
                         "EDA", "EEG", "EMG", "RGB video", "Temperature"]

        if not os.path.exists("pipe"):
            open("pipe", "w").write("Busy")
            sleep(30)
            [channel_service.save_channel(ChannelIn(type=channel_type)) for channel_type in channel_types]
            os.remove("pipe")
