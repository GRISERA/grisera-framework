from typing import Union

from channel.channel_service import ChannelService
from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from recording.recording_service import RecordingService
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_channel.registered_channel_model import BasicRegisteredChannelOut, RegisteredChannelsOut, \
    RegisteredChannelOut, RegisteredChannelIn
from models.not_found_model import NotFoundByIdModel
from registered_data.registered_data_service import RegisteredDataService


class RegisteredChannelServiceGraphDB(RegisteredChannelService):
    """
    Object to handle logic of registered channels requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    channel_service (ChannelService): Service to send channel requests
    registered_data_service (RegisteredDataService): Service to send registered data requests
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.channel_service: ChannelService = None
        self.registered_data_service: RegisteredDataService = None
        self.recording_service: RecordingService = None

    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to create new registered channel

        Args:
            registered_channel (RegisteredChannelIn): Registered channel to be added

        Returns:
            Result of request as registered channel object
        """
        node_response = self.graph_api_service.create_node("Registered Channel")

        if node_response["errors"] is not None:
            return RegisteredChannelOut(errors=node_response["errors"])
        registered_channel_id = node_response["id"]

        if registered_channel.channel_id is not None and \
                type(self.channel_service.get_channel(registered_channel.channel_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=registered_channel_id,
                                                        end_node=registered_channel.channel_id,
                                                        name="hasChannel")
        if registered_channel.registered_data_id is not None and \
                type(self.registered_data_service.get_registered_data(registered_channel.registered_data_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=registered_channel_id,
                                                        end_node=registered_channel.registered_data_id,
                                                        name="hasRegisteredData")

        return self.get_registered_channel(registered_channel_id)

    def get_registered_channels(self):
        """
        Send request to graph api to get registered channels

        Returns:
            Result of request as list of registered channels objects
        """
        get_response = self.graph_api_service.get_nodes("`Registered Channel`")

        registered_channels = []

        for registered_channel_node in get_response["nodes"]:
            properties = {'id': registered_channel_node['id']}
            for property in registered_channel_node["properties"]:
                if property["key"] == "age":
                    properties[property["key"]] = property["value"]
            registered_channel = BasicRegisteredChannelOut(**properties)
            registered_channels.append(registered_channel)

        return RegisteredChannelsOut(registered_channels=registered_channels)

    def get_registered_channel(self, registered_channel_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given registered channel

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            registered_channel_id (int | str): identity of registered channel

        Returns:
            Result of request as registered channel object
        """
        get_response = self.graph_api_service.get_node(registered_channel_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=registered_channel_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Registered Channel":
            return NotFoundByIdModel(id=registered_channel_id, errors="Node not found.")

        registered_channel = create_stub_from_response(get_response)

        if depth != 0:
            registered_channel["recordings"] = []
            registered_channel["channel"] = None
            registered_channel["registeredData"] = None

            relations_response = self.graph_api_service.get_node_relationships(registered_channel_id)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == registered_channel_id and relation["name"] == "hasRegisteredChannel":
                    registered_channel["recordings"].append(self.recording_service.
                                                            get_recording(relation["start_node"], depth - 1))
                else:
                    if relation["start_node"] == registered_channel_id and relation["name"] == "hasChannel":
                        registered_channel["channel"] = self.channel_service. \
                            get_channel(relation["end_node"], depth - 1)
                    else:
                        if relation["start_node"] == registered_channel_id and relation["name"] == "hasRegisteredData":
                            registered_channel["registeredData"] = self.registered_data_service. \
                                get_registered_data(relation["start_node"], depth - 1)

            return RegisteredChannelOut(**registered_channel)
        else:
            return BasicRegisteredChannelOut(**registered_channel)

    def delete_registered_channel(self, registered_channel_id: Union[int, str]):
        """
        Send request to graph api to delete given registered channel

        Args:
            registered_channel_id (int | str): identity of registered channel

        Returns:
            Result of request as registered channel object
        """
        get_response = self.get_registered_channel(registered_channel_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(registered_channel_id)
        return get_response

    def update_registered_channel_relationships(self, registered_channel_id: Union[int, str],
                                                registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to update given registered channel

        Args:
            registered_channel_id (int | str): identity of registered channel
            registered_channel (RegisteredChannelIn): Relationships to update

        Returns:
            Result of request as registered channel object
        """
        get_response: RegisteredChannelOut
        get_response = self.get_registered_channel(registered_channel_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if registered_channel.channel_id is not None and \
                type(self.channel_service.get_channel(registered_channel.channel_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=registered_channel_id,
                                                        end_node=registered_channel.channel_id,
                                                        name="hasChannel")
        if registered_channel.registered_data_id is not None and \
                type(self.registered_data_service.get_registered_data(registered_channel.registered_data_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=registered_channel_id,
                                                        end_node=registered_channel.registered_data_id,
                                                        name="hasRegisteredData")

        return self.get_registered_channel(registered_channel_id)
