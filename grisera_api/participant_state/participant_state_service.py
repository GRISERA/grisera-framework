from graph_api_service import GraphApiService
from participant.participant_service import ParticipantService
from personality.personality_service import PersonalityService
from appearance.appearance_service import AppearanceService
from participant_state.participant_state_model import ParticipantStatePropertyIn, BasicParticipantStateOut, \
    ParticipantStatesOut, ParticipantStateOut, ParticipantStateIn, ParticipantStateRelationIn
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ParticipantStateService:
    """
    Object to handle logic of participant state requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        participant_service (ParticipantService): Service to manage participant models
        appearance_service (AppearanceService): Service to manage appearance models
        personality_service (PersonalityService): Service to manage personality models
    """
    graph_api_service = GraphApiService()
    participant_service = ParticipantService()
    appearance_service = AppearanceService()
    personality_service = PersonalityService()

    def save_participant_state(self, participant_state: ParticipantStateIn):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """
        print("save_participant_state not implemented yet")

    def get_participant_states(self):
        """
        Send request to graph api to get participant states

        Returns:
            Result of request as list of participant states objects
        """
        print("get_participant_states not implemented yet")

    def get_participant_state(self, participant_state_id: int):
        """
        Send request to graph api to get given participant state

        Args:
            participant_state_id (int): Id of participant state

        Returns:
            Result of request as participant state object
        """
        print("get_participant_state not implemented yet")

    def delete_participant_state(self, participant_state_id: int):
        """
        Send request to graph api to delete given participant state

        Args:
            participant_state_id (int): Id of participant state

        Returns:
            Result of request as participant state object
        """
        print("delete_participant_state not implemented yet")

    def update_participant_state(self, participant_state_id: int, participant_state: ParticipantStatePropertyIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int): Id of participant state
            participant_state (ParticipantStatePropertyIn): Properties to update

        Returns:
            Result of request as participant state object
        """
        print("update_participant_state not implemented yet")

    def update_participant_state_relationships(self, participant_state_id: int,
                                               participant_state: ParticipantStateRelationIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int): Id of participant state
            participant_state (ParticipantStateRelationIn): Relationships to update

        Returns:
            Result of request as participant state object
        """
        print("update_participant_state_relationships not implemented yet")
