from graph_api_service import GraphApiService
from activity_execution.activity_execution_service import ActivityExecutionService
from participant_state.participant_state_service import ParticipantStateService
from participation.participation_model import ParticipationIn, ParticipationOut, ParticipationsOut, \
    BasicParticipationOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ParticipationService:
    """
    Object to handle logic of participation requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_execution_service (ActivityExecutionService): Service to send activity execution requests
    participant_state_service (ParticipantStateService): Service to send participant state requests
    """
    graph_api_service = GraphApiService()
    activity_execution_service = ActivityExecutionService()
    participant_state_service = ParticipantStateService()

    def save_participation(self, participation: ParticipationIn):
        """
        Send request to graph api to create new participation

        Args:
            participation (ParticipationIn): Participation to be added

        Returns:
            Result of request as participation object
        """
        raise Exception("save_participation not implemented yet")

    def get_participations(self):
        """
        Send request to graph api to get participations
        Returns:
            Result of request as list of participation objects
        """
        raise Exception("get_participations not implemented yet")

    def get_participation(self, participation_id: int):
        """
        Send request to graph api to get given participation
        Args:
            participation_id (int): Id of participation
        Returns:
            Result of request as participation object
        """
        raise Exception("get_participation not implemented yet")

    def delete_participation(self, participation_id: int):
        """
        Send request to graph api to delete given participation
        Args:
            participation_id (int): Id of participation
        Returns:
            Result of request as participation object
        """
        raise Exception("delete_participation not implemented yet")

    def update_participation_relationships(self, participation_id: int,
                                           participation: ParticipationIn):
        """
        Send request to graph api to update given participation relationships
        Args:
            participation_id (int): Id of participation
            participation (ParticipationIn): Relationships to update
        Returns:
            Result of request as participation object
        """
        raise Exception("update_participation_relationships not implemented yet")
