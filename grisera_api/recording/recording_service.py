from graph_api_service import GraphApiService
from recording.recording_model import RecordingsIn, RecordingsOut, RecordingIn, RecordingOut
from participation.participation_service import ParticipationService, ParticipationOut


class RecordingService:
    """
    Object to handle logic of recordings requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        participation_service (ParticipationService): Service used to communicate with Participation
    """
    graph_api_service = GraphApiService()
    participation_service = ParticipationService()
    
    def save_recording(self, recording: RecordingIn):
        """
        Send request to graph api to create new recording

        Args:
            recording (RecordingIn): Recording to be created

        Returns:
            Result of request as recording object
        """
        node_response_recording = self.graph_api_service.create_node("Recording")

        if node_response_recording["errors"] is not None:
            return RecordingOut(errors=node_response_recording["errors"])

        recording_id = node_response_recording["id"]

        node_response_participation = self.participation_service.save_participation()

        participation_id = node_response_participation.id

        self.graph_api_service.create_relationships(participation_id, recording.activity_id,
                                                    "hasActivity")
        self.graph_api_service.create_relationships(participation_id, recording.participant_state_id,
                                                    "hasParticipantState")
        self.graph_api_service.create_relationships(recording_id, participation_id,
                                                    "hasParticipation")

        return RecordingOut(activity_id=recording.activity_id, participant_state_id=recording.participant_state_id,
                            id=recording_id)

    def save_recordings(self, recordings: RecordingsIn):
        """
        Send request to graph api to create new recordings

        Args:
            recordings (RecordingsIn): Recordings to be added

        Returns:
            Result of request as recordings object
        """
        recordings = [self.save_recording(RecordingIn(participant_state_id=recordings.participant_state_id,
                                                      activity_id=activity))
                      for activity in recordings.activities]

        return RecordingsOut(recordings=recordings)
