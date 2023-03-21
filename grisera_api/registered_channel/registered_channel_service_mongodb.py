from mongo_service import mongo_api_service
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

        registered_channel_id = mongo_api_service.create_document(registered_channel)

        return self.get_registered_channel(registered_channel_id)

    def get_registered_channels(self, query: dict = {}):
        """
        Send request to mongo api to get registered channels

        Args:
            query (dict): Query for mongo request. Gets all registered channels by default.

        Returns:
            Result of request as list of registered channels objects
        """
        registered_channels = mongo_api_service.load_documents(
            BasicRegisteredChannelOut, query=query
        )
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
            source (str): internal argument for mongo services, used to tell the direction of model fetching.
                          i.e. if for this service, if source="recording", it means that this method was invoked
                          from recording service, so recording model will not be fetched, as it is already in response.

        Returns:
            Result of request as registered channel object
        """
        registered_channel = mongo_api_service.load_document(
            registered_channel_id, RegisteredChannelOut
        )

        if registered_channel is NotFoundByIdModel:
            return registered_channel

        self._add_related_documents(registered_channel, depth, source)

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

        mongo_api_service.delete_document(registered_channel)
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
        existing_registered_channel = self.get_registered_channel(registered_channel_id)

        if type(existing_registered_channel) is NotFoundByIdModel:
            return existing_registered_channel

        related_channel = self.channel_service.get_channel(
            registered_channel.channel_id
        )
        related_channel_exists = type(related_channel) is not NotFoundByIdModel
        if related_channel_exists:
            mongo_api_service.update_document(
                registered_channel_id,
                RegisteredChannelIn(channel_id=registered_channel.channel_id),
            )

        related_registered_channel = self.registered_data_service.get_channel(
            registered_channel.registered_data_id
        )
        related_registered_channel_exists = (
            type(related_registered_channel) is not NotFoundByIdModel
        )
        if related_registered_channel_exists:
            mongo_api_service.update_document(
                registered_channel_id,
                RegisteredChannelIn(
                    registered_data_id=registered_channel.registered_data_id
                ),
            )

        return self.get_registered_channel(registered_channel_id)

    def get_registered_channels_traverse(self, query: dict, depth: int, source: str):
        """
        Send request to mongo api to get registered channels with related models

        Args:
            query (dict): Query for mongo request. Gets all registered channels by default.
            depth (int): this attribute specifies how many models will be traversed to create the response.
                         for depth=0, only no further models will be travesed.
            source (str): internal argument for mongo services, used to tell the direction of model fetching.

        Returns:
            Result of request as list of registered channels
        """
        registered_channels = mongo_api_service.load_documents(
            RegisteredChannelOut, query=query
        )

        for rc in registered_channels:
            self._add_related_documents(rc, depth, source)

        return registered_channels

    def _add_related_documents(self, registered_channel: dict, depth: int, source: str):
        if depth > 0:
            self._add_related_recordings(registered_channel, depth, source)
            self._add_related_channel(registered_channel, depth, source)
            self._add_related_registered_data(registered_channel, depth, source)

    def _add_related_recordings(
        self, registered_channel: dict, depth: int, source: str
    ):
        if source != "recording":
            registered_channel[
                "recorgings"
            ] = self.recording_service.get_recordings_traverse(
                {"registered_channel": registered_channel["id"]},
                depth=depth - 1,
                source="registered_channel",
            )

    def _add_related_channel(self, registered_channel: dict, depth: int, source: str):
        has_related_channel = registered_channel["channel_id"] is not None
        if source != "channel" and has_related_channel:
            registered_channel["channel"] = self.channel_service.get_channel_traverse(
                channel_id=registered_channel["channel_id"],
                depth=depth - 1,
                source="registered_channel",
            )

    def _add_related_registered_data(
        self, registered_channel: dict, depth: int, source: str
    ):
        has_related_rd = registered_channel["registered_data_id"] is not None
        if source != "registered_data" and has_related_rd:
            registered_channel[
                "registered_data"
            ] = self.channel_service.get_registered_data(
                registered_data_id=registered_channel["registered_data_id"],
                depth=depth - 1,
                source="registered_channel",
            )
