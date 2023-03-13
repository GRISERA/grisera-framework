from typing import Union
from channel.channel_service import ChannelService
from channel.channel_model import ChannelIn, ChannelOut, ChannelsOut, BasicChannelOut
from models.not_found_model import NotFoundByIdModel
from mongo_api_service import mongo_api_service


class ChannelServiceMongoDB(ChannelService):
    """
    Object to handle logic of channel requests

    Attributes:
    registered_channel_service (RegisteredChannelService): Service to send registered channel requests
    """

    def __init__(self, registered_channel_service):
        self.registered_channel_service = registered_channel_service

    def save_channel(self, channel: ChannelIn):
        """
        Send request to mongo api to create new channel

        Args:
            channel (ChannelIn): Channel to be added

        Returns:
            Result of request as channel object
        """
        channel_id = mongo_api_service.create_document("channels", channel)

        return self.get_channel(channel_id)

    def get_channels(self):
        """
        Send request to mongo api to get all channels

        Returns:
            Result of request as ChannelsOut object
        """
        channels = mongo_api_service.load_documents({}, "channels", BasicChannelOut)
        result = [BasicChannelOut(**c) for c in channels]
        return ChannelsOut(channels=result)

    def get_channel(self, channel_id: Union[str, int]):
        """
        Send request to mongo api to get given channel

        Args:
            channel_id (int): Id of channel

        Returns:
            Result of request as channel object
        """
        channel = self.get_channel_traverse(channel_id, 0, "")
        if channel is NotFoundByIdModel:
            return channel
        return ChannelOut(*channel)

    def get_channel_traverse(self, channel_id: int, depth: int, source: str):
        """
        Send request to mongo api to get given channel with related models

        Args:
            channel_id (int): Id of channel
            depth (int): this attribute specifies how many models will be traversed to create the response.
                         for depth=0, only no further models will be travesed.
            source (str): internal argument for mongo services, used to tell the direction of model fetching.

        Returns:
            Result of request as channel dictionary
        """
        channel = mongo_api_service.load_document(channel_id, "channels", ChannelOut)

        if channel is NotFoundByIdModel:
            return channel

        self._add_related_registered_channels(channel, depth, source)

        return channel

    def _add_related_registered_channels(self, channel: dict, depth: int, source: str):
        if source != "recording" and depth > 0:
            channel[
                "registered_channels"
            ] = self.registered_channel_service.get_registered_channels_traverse(
                {"channel_id": channel["id"]},
                depth=depth - 1,
                source="channel",
            )
