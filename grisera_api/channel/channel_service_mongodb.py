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

    def get_channels(self, query: dict = {}):
        """
        Send request to mongo api to get channels

        Args:
            query (dict): Query for mongo request. Gets all channels by default.

        Returns:
            Result of request as list of channel objects
        """
        channels = mongo_api_service.load_documents(query, "channels", BasicChannelOut)
        result = [BasicChannelOut(**c) for c in channels]

        return ChannelsOut(channels=result)

    def get_channel(self, channel_id: int, depth: int = 0, source: str = ""):
        """
        Send request to mongo api to get given channel

        Args:
            channel_id (int): Id of channel
            depth (int): this attribute specifies how many models will be traversed to create the response.
                         for depth=0, only no further models will be travesed.
            source (str): internal argument for mongo services, used to tell the direcion of model fetching.

        Returns:
            Result of request as registered channel object
        """
        channel = mongo_api_service.load_document(channel_id, "channels", ChannelOut)

        if channel is NotFoundByIdModel:
            return channel

        if depth == 0:
            return ChannelOut(**channel)

        if source != "registered_channel":
            channel[
                "registered_channels"
            ] = self.registered_channel_service.get_registered_channels(
                query={"channel_id": channel_id}
            ).registered_channels

        return ChannelOut(**channel)
