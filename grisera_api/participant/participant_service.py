from graph_api_service import GraphApiService
from participant.participant_model import ParticipantIn, ParticipantOut


class ParticipantService:
    """
    Object to handle logic of participants requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_participant(self, participant: ParticipantIn):
        """
        Send request to graph api to create new participant

        Args:
            participant (ParticipantIn): Participant to be added

        Returns:
            Result of request as participant object
        """
        response = self.graph_api_service.create_participant(participant)

        if response["errors"] is not None:
            return ParticipantOut(errors=response["errors"])
        participant_id = response["id"]
        return ParticipantOut(id=participant_id)
