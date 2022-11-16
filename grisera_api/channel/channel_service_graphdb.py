from graph_api_service import GraphApiService
from channel.channel_model import ChannelIn, ChannelOut, ChannelsOut, BasicChannelOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ChannelServiceGraphDB:
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
            return ChannelOut(type=channel.type, errors=properties_response["errors"])

        return ChannelOut(type=channel.type,  id=channel_id)

    def get_channels(self):
        """
        Send request to graph api to get all channels

        Returns:
            Result of request as list of channel objects
        """
        get_response = self.graph_api_service.get_nodes("Channel")
        if get_response["errors"] is not None:
            return ChannelsOut(errors=get_response["errors"])
        channels = [BasicChannelOut(id=channel["id"], type=channel["properties"][0]["value"])
                    for channel in get_response["nodes"]]

        return ChannelsOut(channels=channels)

    def get_channel(self, channel_id: int):
        """
        Send request to graph api to get given channel

        Args:
        channel_id (int): Id of channel

        Returns:
            Result of request as channel object
        """
        get_response = self.graph_api_service.get_node(channel_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=channel_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Channel":
            return NotFoundByIdModel(id=channel_id, errors="Node not found.")

        channel = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            channel[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(channel_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == channel_id:
                channel['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                name=relation["name"], relation_id=relation["id"]))
            else:
                channel['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                         name=relation["name"],
                                                                         relation_id=relation["id"]))

        return ChannelOut(**channel)
