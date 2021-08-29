from graph_api_service import GraphApiService
from recording.recording_model import RecordingIn, RecordingOut


class RecordingService:
    """
    Object to handle logic of recording requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_recording(self, recording: RecordingIn):
        """
        Send request to graph api to create new recording node

        Args:
            recording (RecordingIn): Recording to be added

        Returns:
            Result of request as recording object
        """
        node_response = self.graph_api_service.create_node("Recording")

        if node_response["errors"] is not None:
            return RecordingOut(participation_id=recording.participation_id,
                                registered_channel_id=recording.registered_channel_id,
                                errors=node_response["errors"])

        recording_id = node_response["id"]
        registered_channel_id = recording.registered_channel_id
        participation_id = recording.participation_id
        recording.registered_channel_id = recording.participation_id = None

        properties_response = self.graph_api_service.create_properties(recording_id, recording)
        if properties_response["errors"] is not None:
            return RecordingOut(participation_id=participation_id,
                                registered_channel_id=registered_channel_id,
                                errors=node_response["errors"])

        self.graph_api_service.create_relationships(recording_id, registered_channel_id,
                                                    "hasRegisteredChannel")
        self.graph_api_service.create_relationships(recording_id, participation_id,
                                                    "hasParticipation")

        return RecordingOut(participation_id=participation_id,
                            registered_channel_id=registered_channel_id,
                            id=recording_id, additional_properties=recording.additional_properties)
