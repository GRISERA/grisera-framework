from graph_api_service import GraphApiService
from channel.channel_model import ChannelIn, ChannelOut, ChannelsOut, BasicChannelOut


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
        create_response = self.graph_api_service.create_node("Channel")

        if create_response["errors"] is not None:
            return ChannelOut(type=channel.type, errors=create_response["errors"])

        channel_id = create_response["id"]
        properties_response = self.graph_api_service.create_properties(channel_id, channel)
        if properties_response["errors"] is not None:
            return ChannelOut(type=channel.type, errors=create_response["errors"])

        return ChannelOut(type=channel.type,  id=channel_id)

    def get_channels(self):
        """
        Send request to graph api to get all channels

        Returns:
            Result of request as list of channel objects
        """
        get_response = self.graph_api_service.get_nodes("Channel")
        if type(get_response["Channel"]) is dict:
            return ChannelsOut(errors=get_response["Channel"])
        channels = [BasicChannelOut(id=channel["id"], type=channel["properties"][0]["value"])
                    for channel in get_response["Channel"]]

        return ChannelsOut(channels=channels)
