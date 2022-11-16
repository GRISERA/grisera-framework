from graph_api_service import GraphApiService
from participation.participation_service import ParticipationService
from registered_channel.registered_channel_service import RegisteredChannelService
from recording.recording_model import RecordingPropertyIn, RecordingRelationIn, RecordingIn, BasicRecordingOut, RecordingOut, RecordingsOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class RecordingService:
    """
    Object to handle logic of recording requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    participation_service (ParticipationService): Service to send participation requests
    registered_channel_service(RegisteredChannelService): Service to send registered channel requests
    """
    graph_api_service = GraphApiService()
    participation_service = ParticipationService()
    registered_channel_service = RegisteredChannelService()

    def save_recording(self, recording: RecordingIn):
        """
        Send request to graph api to create new recording node

        Args:
            recording (RecordingIn): Recording to be added

        Returns:
            Result of request as recording object
        """
        raise Exception("save_recording not implemented yet")

    def get_recordings(self):
        """
        Send request to graph api to get recordings
        Returns:
            Result of request as list of recordings objects
        """
        raise Exception("get_recordings not implemented yet")

    def get_recording(self, recording_id: int):
        """
        Send request to graph api to get given recording
        Args:
            recording_id (int): Id of recording
        Returns:
            Result of request as recording object
        """
        raise Exception("get_recording not implemented yet")

    def delete_recording(self, recording_id: int):
        """
        Send request to graph api to delete given recording
        Args:
            recording_id (int): Id of recording
        Returns:
            Result of request as recording object
        """
        raise Exception("delete_recording not implemented yet")

    def update_recording(self, recording_id: int, recording: RecordingPropertyIn):
        """
        Send request to graph api to update given participant state
        Args:
            recording_id (int): Id of participant state
            recording (RecordingPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        raise Exception("update_recording not implemented yet")
    
    def update_recording_relationships(self, recording_id: int,
                                       recording: RecordingIn):
        """
        Send request to graph api to update given recording
        Args:
            recording_id (int): Id of recording
            recording (RecordingIn): Relationships to update
        Returns:
            Result of request as recording object
        """
        raise Exception("update_recording_relationships not implemented yet")
