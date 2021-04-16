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
        node_response = self.graph_api_service.create_node("Participant")

        if node_response["errors"] is not None:
            return ParticipantOut(errors=node_response["errors"])

        participant_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(participant_id, participant)
        if properties_response["errors"] is not None:
            return ParticipantOut(errors=properties_response["errors"])

        return ParticipantOut(age=participant.age, sex=participant.sex, beard=participant.beard,
                              moustache=participant.moustache, glasses=participant.glasses,
                              disorder=participant.disorder, disorder_type=participant.disorder_type,
                              id=participant_id)
