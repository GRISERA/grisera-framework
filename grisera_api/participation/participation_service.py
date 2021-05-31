from graph_api_service import GraphApiService
from participation.participation_model import ParticipationsIn, ParticipationsOut, ParticipationIn, ParticipationOut


class ParticipationService:
    """
    Object to handle logic of participation requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_participation(self, participation: ParticipationIn):
        """
        Send request to graph api to create new participation

        Args:
            participation (ParticipationIn): Participation to be created

        Returns:
            Result of request as participation object
        """
        node_response = self.graph_api_service.create_node("Participation")

        if node_response["errors"] is not None:
            return ParticipationOut(errors=node_response["errors"])

        participation_id = node_response["id"]

        self.graph_api_service.create_relationships(participation_id, participation.activity_id,
                                                    "hasActivity")
        self.graph_api_service.create_relationships(participation_id, participation.participant_state_id,
                                                    "hasParticipantState")

        return ParticipationOut(activity_id=participation.activity_id,
                                participant_state_id=participation.participant_state_id,
                                id=participation_id)

    def save_participations(self, participations: ParticipationsIn):
        """
        Send request to graph api to create new participations

        Args:
            participations (ParticipationsIn): Participations to be added

        Returns:
            Result of request as participations object
        """
        participations = [
            self.save_participation(ParticipationIn(participant_state_id=participations.participant_state_id,
                                                    activity_id=activity))
            for activity in participations.activities]

        return ParticipationsOut(participations=participations)
