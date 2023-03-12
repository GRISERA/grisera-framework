from mongo_api_service import mongo_api_service
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_channel.registered_channel_model import (
    RegisteredChannelOut,
    RegisteredChannelIn,
    BasicRegisteredChannelOut,
    RegisteredChannelsOut,
)
from models.not_found_model import NotFoundByIdModel


class RegisteredChannelServiceMongoDB(RegisteredChannelService):
    """
    Object to handle logic of registered channels requests

    Attributes:
    channel_service (ChannelServiceMongoDB): Service to send channel requests
    registered_data_service (RegisteredDataServiceMongoDB): Service to send registered data requests
    recording_service (RecordingServiceMongoDB): Service to send recording requests
    """

    def __init__(self, channel_service, registered_data_service, recording_service):
        self.channel_service = channel_service()
        self.registered_data_service = registered_data_service()
        self.recording_service = recording_service()

    def save_registered_channel(self, registered_channel: RegisteredChannelIn):
        """
        Send request to mongo api to create new registered channel

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

    def get_registered_channels(self, query: dict = {}):
        """
        Send request to mongo api to get registered channels

        Args:
            query (dict): Query for mongo request. Gets all registered channels by default.

        Returns:
            Result of request as list of registered channels objects
        """
        registered_channels = mongo_api_service.db.registered_channels.find(query)
        result = [BasicRegisteredChannelOut(**rc) for rc in registered_channels]

        return RegisteredChannelsOut(registered_channels=result)

    def get_registered_channel(
        self, registered_channel_id: int, depth: int = 0, source: str = ""
    ):
        """
        Send request to mongo api to get given registered channel

        Args:
            registered_channel_id (int): Id of registered channel
            depth (int): this attribute specifies how many models will be traversed to create the response.
                         for depth=0, only no further models will be travesed.
            source (str): internal argument for mongo services, used to tell the direcion of model fetching.
                          i.e. if for this service, if source="recording", it means that this method was invoked
                          from recording service, so recording model will not be fetched, as it is already in response.

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
        Send request to mongo api to delete given registered channel

        Args:
            registered_channel_id (int): Id of registered channel

        Returns:
            Result of request as registered channel object
        """
        registered_channel = self.get_registered_channel(registered_channel_id)

        if registered_channel is None:
            return NotFoundByIdModel(
                id=registered_channel_id,
                errors={"errors": "registered channel not found"},
            )

        mongo_api_service.db.registered_channels.delete_one(
            {"id": registered_channel_id}
        )
        return registered_channel

    def update_registered_channel_relationships(
        self, registered_channel_id: int, registered_channel: RegisteredChannelIn
    ):
        """
        Send request to mongo api to update given registered channel

        Args:
            registered_channel_id (int): Id of registered channel
            registered_channel (RegisteredChannelIn): Document to update

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
            mongo_api_service.db.registered_channels.update_one(
                {"id": registered_channel_id},
                {"channel_id": registered_channel.channel_id},
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
            mongo_api_service.db.registered_channels.update_one(
                {"id": registered_channel_id},
                {"registered_data_id": registered_channel.registered_data_id},
            )

        return self.get_registered_channel(registered_channel_id)
