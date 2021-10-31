from graph_api_service import GraphApiService
from participant.participant_service import ParticipantService
from participant_state.participant_state_model import ParticipantStateIn, ParticipantStateOut


class ParticipantStateService:
    """
    Object to handle logic of participant state requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        participant_service (ParticipantService): Service to manage participant models
    """
    graph_api_service = GraphApiService()
    participant_service = ParticipantService()

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

        participant = None
        if participant_state.participant is not None:
            participant = self.participant_service.save_participant(participant=participant_state.participant)
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant.id,
                                                        name="hasParticipant")

        if participant_state.personality_id is not None:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.personality_id,
                                                        name="hasPersonality")
        if participant_state.appearance_id is not None:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.appearance_id,
                                                        name="hasAppearance")

        properties_response = self.graph_api_service.create_properties(participant_state_id, participant_state)
        if properties_response["errors"] is not None:
            return ParticipantStateOut(errors=properties_response["errors"])

        return ParticipantStateOut(participant=participant, age=participant_state.age, id=participant_state_id,
                                   additional_properties=participant_state.additional_properties)
