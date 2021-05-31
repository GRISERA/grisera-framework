from graph_api_service import GraphApiService
from channel.channel_model import ChannelIn, ChannelOut


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
