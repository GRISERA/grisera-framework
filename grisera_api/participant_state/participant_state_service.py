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
    Abstract class to handle logic of participant state requests

    """

    def save_participant_state(self, participant_state: ParticipantStateIn):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """
        raise Exception("save_participant_state not implemented yet")

    def get_participant_states(self):
        """
        Send request to graph api to get participant states

        Returns:
            Result of request as list of participant states objects
        """
        raise Exception("get_participant_states not implemented yet")

    def get_participant_state(self, participant_state_id: int):
        """
        Send request to graph api to get given participant state

        Args:
            participant_state_id (int): Id of participant state

        Returns:
            Result of request as participant state object
        """
        raise Exception("get_participant_state not implemented yet")

    def delete_participant_state(self, participant_state_id: int):
        """
        Send request to graph api to delete given participant state

        Args:
            participant_state_id (int): Id of participant state

        Returns:
            Result of request as participant state object
        """
        raise Exception("delete_participant_state not implemented yet")

    def update_participant_state(self, participant_state_id: int, participant_state: ParticipantStatePropertyIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int): Id of participant state
            participant_state (ParticipantStatePropertyIn): Properties to update

        Returns:
            Result of request as participant state object
        """
        raise Exception("update_participant_state not implemented yet")

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
        raise Exception("update_participant_state_relationships not implemented yet")
