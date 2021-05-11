from graph_api_service import GraphApiService
from participant_state.participant_state_model import ParticipantStateIn, ParticipantStateOut


class ParticipantStateService:
    """
    Object to handle logic of participant state requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_participant_state(self, participant_state: ParticipantStateIn):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """
        node_response = self.graph_api_service.create_node("`Participant State`")

        if node_response["errors"] is not None:
            return ParticipantStateOut(errors=node_response["errors"])

        participant_state_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(participant_state_id, participant_state)
        if properties_response["errors"] is not None:
            return ParticipantStateOut(errors=properties_response["errors"])

        return ParticipantStateOut(participant=participant_state.participant, age=participant_state.age,
                                   beard=participant_state.beard, moustache=participant_state.moustache,
                                   glasses=participant_state.glasses, id=participant_state_id,
                                   additional_properties=participant_state.additional_properties)
