from mongo_service.service_mixins import (
    GenericMongoServiceMixin,
)
from graph_api_service import GraphApiService
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from recording.recording_service import RecordingService
from registered_channel.registered_channel_service_graphdb import (
    RegisteredChannelServiceGraphDB,
)
from recording.recording_model import (
    RecordingPropertyIn,
    RecordingRelationIn,
    RecordingIn,
    BasicRecordingOut,
    RecordingOut,
    RecordingsOut,
)
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from mongo_service import mongo_api_service


class RecordingServiceMongoDB(RecordingService, GenericMongoServiceMixin):
    """
    Object to handle logic of recording requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    participation_service (ParticipationService): Service to send participation requests
    registered_channel_service(RegisteredChannelService): Service to send registered channel requests
    """

    def __init__(self):
        self.model_out_class = RecordingOut
        self.registered_channel_service = None
        self.observable_information_service = None
        self.participation_service = None

    def save_recording(self, recording: RecordingIn):
        """
        Send request to mongo api to create new recording document

        Args:
            recording (RecordingIn): Recording to be added

        Returns:
            Result of request as recording object
        """
        participation = self.participation_service.get_participation(
            recording.participation_id
        )
        participation_exists = participation is not NotFoundByIdModel
        if recording.participation_id is not None and not participation_exists:
            return RecordingOut(errors={"errors": "given participation does not exist"})

        related_registered_channel = (
            self.registered_channel_service.get_registered_channel(
                recording.registered_channel_id
            )
        )
        registered_channel_exists = related_registered_channel is not NotFoundByIdModel
        if (
            recording.registered_channel_id is not None
            and not registered_channel_exists
        ):
            return RecordingOut(
                errors={"errors": "given registered channel does not exist"}
            )

        return self.create(recording)

    def get_recordings(self, query: dict = {}):
        """
        Send request to graph api to get recordings
        Returns:
            Result of request as list of recordings objects
        """
        results_dict = self.get_multiple(query)
        results = [BasicRecordingOut(**result) for result in results_dict]
        return RecordingsOut(registered_channels=results)

    def get_recording(self, recording_id: int, depth: int = 0, source: str = ""):
        """
        Send request to mongo api to get given recording. This method uses mixin get implementation.

        Args:
            recording_id (int): Id of registered channel
            depth (int): this attribute specifies how many models will be traversed to create the response.
                         for depth=0, only no further models will be travesed.
            source (str): internal argument for mongo services, used to tell the direction of model fetching.
                          i.e. if for this service, if source="registered_channel", it means that this method was invoked
                          from registered channel service, so registered channel model will not be fetched, as it is already
                          in response.

        Returns:
            Result of request as registered channel object
        """
        self.get_single(recording_id, depth, source)

    def delete_recording(self, recording_id: int):
        """
        Send request to mongo api to delete given recording
        Args:
            recording_id (int): Id of recording
        Returns:
            Result of request as recording object
        """
        return self.delete(recording_id)

    def update_recording(self, recording_id: int, recording: RecordingPropertyIn):
        """
        Send request to graph api to update given participant state
        Args:
            recording_id (int): Id of participant state
            recording (RecordingPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        return self.update(recording_id, recording)

    def update_recording_relationships(self, recording_id: int, recording: RecordingIn):
        """
        Send request to graph api to update given recording
        Args:
            recording_id (int): Id of recording
            recording (RecordingIn): Relationships to update
        Returns:
            Result of request as recording object
        """
        existing_recording = self.get_recording(recording_id)

        if type(existing_recording) is NotFoundByIdModel:
            return existing_recording

        related_registered_channel = self.registered_channel_service.get_channel(
            recording.registered_channel_id
        )
        related_registered_channel_exists = (
            type(related_registered_channel) is not NotFoundByIdModel
        )
        if related_registered_channel_exists:
            mongo_api_service.update_document(
                recording_id,
                RecordingIn(registered_channel_id=recording.registered_channel_id),
            )

        related_participation = self.participation_service.get_participation(
            recording.participation_id
        )
        related_participation_exists = (
            type(related_participation) is not NotFoundByIdModel
        )
        if related_participation_exists:
            mongo_api_service.update_document(
                recording_id,
                RecordingIn(participation_id=recording.participation_id),
            )

        return self.get_recording(recording_id)

    def _add_related_documents(self, recording: dict, depth: int, source: str):
        if depth > 0:
            self._add_related_registered_channel(recording, depth, source)
            self._add_related_participation(recording, depth, source)
            self._add_related_observable_informations(recording, depth, source)

    def _add_related_registered_channel(self, recording: dict, depth: int, source: str):
        has_related_rc = recording["registered_channel_id"] is not None
        if source != "registered_channel" and has_related_rc:
            recording[
                "registered_channel"
            ] = self.registered_channel_service.get_single_dict(
                recording["registered_channel_id"],
                depth=depth - 1,
                source="recording",
            )

    def _add_related_participation(self, recording: dict, depth: int, source: str):
        has_participation = recording["participation_id"] is not None
        if source != "participation" and has_participation:
            recording["participation"] = self.participation_service.get_single_dict(
                channel_id=recording["participation_id"],
                depth=depth - 1,
                source="recording",
            )

    def _add_related_observable_informations(
        self, recording: dict, depth: int, source: str
    ):
        """
        Oservable information is embeded within recording model
        """
        has_observable_informations = recording["obervable_informations"] is not None
        if source != "obervable_information" and has_observable_informations:
            for oi in recording["obervable_informations"]:
                self.observable_information_service._add_related_documents(
                    oi, depth - 1, "recording"
                )
