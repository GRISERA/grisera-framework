from graph_api_service import GraphApiService
from modality.modality_model import ModalityIn, ModalityOut, ModalitiesOut, BasicModalityOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


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
        print("save_modality not implemented yet")

    def get_modalities(self):
        """
        Send request to graph api to get all modalities

        Returns:
            Result of request as list of modality objects
        """
        print("get_modalities not implemented yet")

    def get_modality(self, modality_id: int):
        """
        Send request to graph api to get given modality

        Args:
        modality_id (int): Id of modality

        Returns:
            Result of request as modality object
        """
        print("get_modality not implemented yet")
