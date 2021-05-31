from graph_api_service import GraphApiService
from participation.participation_model import ParticipationIn, ParticipationOut


class ParticipationService:
    """
    Object to handle logic of participation requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_participation(self):
        """
        Send request to graph api to create new participation

        Args:

        Returns:
            Result of request as participation object
        """
        node_response = self.graph_api_service.create_node("Participation")

        if node_response["errors"] is not None:
            return ParticipationOut(errors=node_response["errors"])

        participation_id = node_response["id"]

        return ParticipationOut(id=participation_id)
