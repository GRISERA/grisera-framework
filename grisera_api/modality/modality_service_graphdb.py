from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from modality.modality_model import ModalityIn, ModalityOut, ModalitiesOut, BasicModalityOut
from modality.modality_service import ModalityService
from models.not_found_model import NotFoundByIdModel
from observable_information.observable_information_service import ObservableInformationService


class ModalityServiceGraphDB(ModalityService):
    """
    Object to handle logic of modality requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.observable_information_service: ObservableInformationService = None

    def save_modality(self, modality: ModalityIn, dataset_name: str):
        """
        Send request to graph api to create new modality

        Args:
            modality (ModalityIn): Modality to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as modality object
        """

        node_response = self.graph_api_service.create_node("Modality", dataset_name)

        if node_response["errors"] is not None:
            return ModalityOut(modality=modality.modality, errors=node_response["errors"])

        modality_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(modality_id, modality, dataset_name)
        if properties_response["errors"] is not None:
            return ModalityOut(modality=modality.modality, errors=properties_response["errors"])

        return ModalityOut(modality=modality.modality, id=modality_id)

    def get_modalities(self, dataset_name: str):
        """
        Send request to graph api to get all modalities

        Args:
            dataset_name (str): name of dataset

        Returns:
            Result of request as list of modality objects
        """
        get_response = self.graph_api_service.get_nodes("Modality", dataset_name)
        modalities = [BasicModalityOut(id=modality["id"], modality=modality["properties"][0]["value"])
                      for modality in get_response["nodes"]]

        return ModalitiesOut(modalities=modalities)

    def get_modality(self, modality_id: Union[int, str], dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given modality

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            modality_id (int | str): identity of modality
            dataset_name (str): name of dataset

        Returns:
            Result of request as modality object
        """
        get_response = self.graph_api_service.get_node(modality_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=modality_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Modality":
            return NotFoundByIdModel(id=modality_id, errors="Node not found.")

        modality = create_stub_from_response(get_response, properties=['modality'])

        if depth != 0:
            modality["observable_informations"] = []
            relations_response = self.graph_api_service.get_node_relationships(modality_id, dataset_name)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == modality_id & relation["name"] == "hasModality":
                    modality['observable_informations'].append(self.observable_information_service.
                                                               get_observable_information(relation["start_node"],
                                                                                          depth - 1))

            return ModalityOut(**modality)
        else:
            return BasicModalityOut(**modality)
