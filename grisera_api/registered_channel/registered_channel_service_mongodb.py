from mongo_api_service import mongo_api_service
from channel.channel_service_mongodb import ChannelServiceMongoDB
from recording.recording_service_mongodb import RecordingServiceMongoDB
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_data.registered_data_service_mongodb import RegisteredDataServiceMongoDB
from registered_channel.registered_channel_model import (
    BasicRegisteredChannelOut,
    RegisteredChannelsOut,
    RegisteredChannelOut,
    RegisteredChannelIn,
)
from models.not_found_model import NotFoundByIdModel


class RegisteredChannelServiceMongoDB(RegisteredChannelService):
    """
    Object to handle logic of registered channels requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    channel_service (ChannelService): Service to send channel requests
    registered_data_service (RegisteredDataService): Service to send registered data requests
    """

    channel_service = ChannelServiceMongoDB()
    registered_data_service = RegisteredDataServiceMongoDB()
    recording_service = RecordingServiceMongoDB()

    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        """
        Send request to graph api to create new registered channel

        Args:
            registered_channel (RegisteredChannelIn): Registered channel to be added

        Returns:
            Result of request as registered channel object
        """
        related_channel = self.channel_service.get_channel(
            registered_channel.channel_id
        )
        channel_exists = related_channel is not NotFoundByIdModel
        if registered_channel.channel_id is not None and not channel_exists:
            return RegisteredChannelOut(
                errors={"errors": "given channel does not exist"}
            )

        related_rd = self.registered_data_service.get_registered_data(
            registered_channel.registered_data_id
        )
        rd_exists = related_rd is not NotFoundByIdModel
        if registered_channel.channel_id is not None and not rd_exists:
            return RegisteredChannelOut(
                errors={"errors": "given registered data does not exist"}
            )

        registered_channel_id = mongo_api_service.db.registered_channels.insert_one(
            {
                "channel_id": registered_channel.channel_id,
                "registered_data_id": registered_channel.registered_data_id,
            }
        )

        return self.get_registered_channel(registered_channel_id)

    def get_registered_channels(self):
        """
        Send request to mongo api to get registered channels

        Returns:
            Result of request as list of registered channels objects
        """
        registered_channels = mongo_api_service.db.registered_channels.find({})
        result = [RegisteredChannelIn(**rc) for rc in registered_channels]

        return result

    def get_registered_channel(
        self, registered_channel_id: int, depth: int = 0, source: str = ""
    ):
        """
        Send request to graph api to get given registered channel

        Args:
            registered_channel_id (int): Id of registered channel

        Returns:
            Result of request as registered channel object
        """
        registered_channel = mongo_api_service.db.registered_channels.find_one(
            {"id": registered_channel_id}
        )

        if registered_channel is None:
            return NotFoundByIdModel(
                id=registered_channel_id,
                errors={"errors": "registered channel not found"},
            )

        if depth == 0:
            return RegisteredChannelOut(**registered_channel)

        if source != "recording":
            registered_channel["recorgings"] = self.recording_service.get_recordings(
                {"registered_channel": registered_channel["id"]},
                depth=depth - 1,
                source="registered_channel",
            )

        has_related_channel = registered_channel["channel_id"] is not None
        if source != "channel" and has_related_channel:
            registered_channel["channel"] = self.channel_service.get_channel(
                channel_id=registered_channel["channel_id"],
                depth=depth - 1,
                source="registered_channel",
            )

        has_related_rd = registered_channel["registered_data_id"] is not None
        if source != "registered_data" and has_related_rd:
            registered_channel[
                "registered_data"
            ] = self.channel_service.get_registered_data(
                registered_data_id=registered_channel["registered_data_id"],
                depth=depth - 1,
                source="registered_channel",
            )

        return RegisteredChannelOut(**registered_channel)

    def delete_registered_channel(self, registered_channel_id: int):
        """
        Send request to graph api to delete given registered channel

        Args:
            registered_channel_id (int): Id of registered channel

        Returns:
            Result of request as registered channel object
        """
        get_response = self.get_registered_channel(registered_channel_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(registered_channel_id)
        return get_response

    def update_registered_channel_relationships(
        self, registered_channel_id: int, registered_channel: RegisteredChannelIn
    ):
        """
        Send request to graph api to update given registered channel

        Args:
            registered_channel_id (int): Id of registered channel
            registered_channel (RegisteredChannelIn): Relationships to update

        Returns:
            Result of request as registered channel object
        """
        get_response = self.get_registered_channel(registered_channel_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if (
            registered_channel.channel_id is not None
            and type(self.channel_service.get_channel(registered_channel.channel_id))
            is not NotFoundByIdModel
        ):
            self.graph_api_service.create_relationships(
                start_node=registered_channel_id,
                end_node=registered_channel.channel_id,
                name="hasChannel",
            )
        if (
            registered_channel.registered_data_id is not None
            and type(
                self.registered_data_service.get_registered_data(
                    registered_channel.registered_data_id
                )
            )
            is not NotFoundByIdModel
        ):
            self.graph_api_service.create_relationships(
                start_node=registered_channel_id,
                end_node=registered_channel.registered_data_id,
                name="hasRegisteredData",
            )

        return self.get_registered_channel(registered_channel_id)
