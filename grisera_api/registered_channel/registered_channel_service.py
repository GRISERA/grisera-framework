from graph_api_service import GraphApiService
from channel.channel_service import ChannelService
from registered_data.registered_data_service import RegisteredDataService
from registered_channel.registered_channel_model import BasicRegisteredChannelOut, RegisteredChannelsOut, \
    RegisteredChannelOut, RegisteredChannelIn
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class RegisteredChannelService:
    """
    Object to handle logic of registered channels requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    channel_service (ChannelService): Service to send channel requests
    registered_data_service (RegisteredDataService): Service to send registered data requests
    """
    graph_api_service = GraphApiService()
    channel_service = ChannelService()
    registered_data_service = RegisteredDataService()

    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to create new registered channel

        Args:
            registered_channel (RegisteredChannelIn): Registered channel to be added

        Returns:
            Result of request as registered channel object
        """
        raise Exception("save_registered_channel not implemented yet")

    def get_registered_channels(self):
        """
        Send request to graph api to get registered channels

        Returns:
            Result of request as list of registered channels objects
        """
        raise Exception("get_registered_channels not implemented yet")

    def get_registered_channel(self, registered_channel_id: int):
        """
        Send request to graph api to get given registered channel

        Args:
            registered_channel_id (int): Id of registered channel

        Returns:
            Result of request as registered channel object
        """
        raise Exception("get_registered_channel not implemented yet")

    def delete_registered_channel(self, registered_channel_id: int):
        """
        Send request to graph api to delete given registered channel

        Args:
            registered_channel_id (int): Id of registered channel

        Returns:
            Result of request as registered channel object
        """
        raise Exception("delete_registered_channel not implemented yet")

    def update_registered_channel_relationships(self, registered_channel_id: int,
                                                registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to update given registered channel

        Args:
            registered_channel_id (int): Id of registered channel
            registered_channel (RegisteredChannelIn): Relationships to update

        Returns:
            Result of request as registered channel object
        """
        raise Exception("update_registered_channel_relationships not implemented yet")
