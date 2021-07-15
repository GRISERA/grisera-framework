from graph_api_service import GraphApiService
from modality.modality_model import ModalityIn, ModalityOut


class ModalityService:
    """
    Object to handle logic of modality requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_modality(self, modality: ModalityIn):
        """
        Send request to graph api to create new modality

        Args:
            modality (ModalityIn): Modality to be added

        Returns:
            Result of request as modality object
        """

        node_response = self.graph_api_service.create_node("Modality")

        if node_response["errors"] is not None:
            return ModalityOut(modality=modality.modality, errors=node_response["errors"])

        modality_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(modality_id, modality)
        if properties_response["errors"] is not None:
            return ModalityOut(errors=properties_response["errors"])

        return ModalityOut(modality=modality.modality, id=modality_id)
