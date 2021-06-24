from graph_api_service import GraphApiService
from registered_channel.registered_channel_model import RegisteredChannelIn, RegisteredChannelOut
from channel.channel_service import ChannelService


class RegisteredChannelService:
    """
    Object to handle logic of registered channels requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        channel_service (ChannelService): Service to send channel requests
    """
    graph_api_service = GraphApiService()
    channel_service = ChannelService()

    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to create new registered channel

        Args:
            registered_channel (RegisteredChannelIn): Registered channel to be added

        Returns:
            Result of request as registered channel object
        """
        node_response = self.graph_api_service.create_node("`Registered channel`")

        if node_response["errors"] is not None:
            return RegisteredChannelOut(channel=registered_channel.channel,
                                        registered_data_id=registered_channel.registered_data_id,
                                        errors=node_response["errors"])
        registered_channel_id = node_response["id"]

        channels = self.channel_service.get_channels().channels
        channel_id = next(channel.id for channel in channels if channel.type == registered_channel.channel)
        self.graph_api_service.create_relationships(start_node=registered_channel_id,
                                                    end_node=channel_id,
                                                    name="hasChannel")
        self.graph_api_service.create_relationships(start_node=registered_channel_id,
                                                    end_node=registered_channel.registered_data_id,
                                                    name="hasRegisteredData")

        return RegisteredChannelOut(channel=registered_channel.channel,
                                    registered_data_id=registered_channel.registered_data_id,
                                    id=registered_channel_id)
