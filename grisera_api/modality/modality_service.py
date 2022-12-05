from graph_api_service import GraphApiService
from modality.modality_model import ModalityIn, ModalityOut, ModalitiesOut, BasicModalityOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ModalityService:
    """
    Abstract class to handle logic of modality requests

    """

    def save_modality(self, modality: ModalityIn):
        """
        Send request to graph api to create new modality

        Args:
            modality (ModalityIn): Modality to be added

        Returns:
            Result of request as modality object
        """
        raise Exception("save_modality not implemented yet")

    def get_modalities(self):
        """
        Send request to graph api to get all modalities

        Returns:
            Result of request as list of modality objects
        """
        raise Exception("get_modalities not implemented yet")

    def get_modality(self, modality_id: int):
        """
        Send request to graph api to get given modality

        Args:
        modality_id (int): Id of modality

        Returns:
            Result of request as modality object
        """
        raise Exception("get_modality not implemented yet")
