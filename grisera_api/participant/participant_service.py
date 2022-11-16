from graph_api_service import GraphApiService
from participant.participant_model import ParticipantIn, ParticipantsOut, BasicParticipantOut, ParticipantOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


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
        raise Exception("save_participant not implemented yet")

    def get_participants(self):
        """
        Send request to graph api to get participants

        Returns:
            Result of request as list of participants objects
        """
        raise Exception("get_participants not implemented yet")

    def get_participant(self, participant_id: int):
        """
        Send request to graph api to get given participant

        Args:
            participant_id (int): Id of participant

        Returns:
            Result of request as participant object
        """
        raise Exception("get_participant not implemented yet")

    def delete_participant(self, participant_id: int):
        """
        Send request to graph api to delete given participant

        Args:
            participant_id (int): Id of participant

        Returns:
            Result of request as participant object
        """
        raise Exception("delete_participant not implemented yet")

    def update_participant(self, participant_id: int, participant: ParticipantIn):
        """
        Send request to graph api to update given participant

        Args:
            participant_id (int): Id of participant
            participant (ParticipantIn): Properties to update

        Returns:
            Result of request as participant object
        """
        raise Exception("update_participant not implemented yet")
