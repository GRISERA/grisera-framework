from graph_api_service import GraphApiService
from channel.channel_model import ChannelIn, ChannelOut, ChannelsOut, BasicChannelOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ChannelService:
    """
    Object to handle logic of channel requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_channel(self, channel: ChannelIn):
        """
        Send request to graph api to create new channel

        Args:
            channel (ChannelIn): Channel to be added

        Returns:
            Result of request as channel object
        """
        raise Exception("save_channel not implemented yet")

    def get_channels(self):
        """
        Send request to graph api to get all channels

        Returns:
            Result of request as list of channel objects
        """
        raise Exception("get_channels not implemented yet")

    def get_channel(self, channel_id: int):
        """
        Send request to graph api to get given channel

        Args:
        channel_id (int): Id of channel

        Returns:
            Result of request as channel object
        """
        raise Exception("get_channel not implemented yet")
