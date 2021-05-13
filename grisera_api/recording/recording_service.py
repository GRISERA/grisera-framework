from graph_api_service import GraphApiService
from recording.recording_model import RecordingsIn, RecordingsOut, RecordingIn, RecordingOut


class RecordingService:
    """
    Object to handle logic of recordings requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_recording(self, recording: RecordingIn):
        """
        Send request to graph api to create new recording

        Args:
            recording (RecordingIn): Recording to be created

        Returns:
            Result of request as recording object
        """
        node_response = self.graph_api_service.create_node("Recording")

        if node_response["errors"] is not None:
            return RecordingOut(errors=node_response["errors"])

        recording_id = node_response["id"]

        self.graph_api_service.create_relationships(recording_id, recording.participant_state_id, "hasRecording")
        self.graph_api_service.create_relationships(recording_id, recording.activity_id, "hasActivity")

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
