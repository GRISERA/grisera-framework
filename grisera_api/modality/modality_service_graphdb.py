from graph_api_service import GraphApiService
from modality.modality_model import ModalityIn, ModalityOut, ModalitiesOut, BasicModalityOut
from modality.modality_service import ModalityService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ModalityServiceGraphDB(ModalityService):
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
            return ModalityOut(modality=modality.modality, errors=properties_response["errors"])

        return ModalityOut(modality=modality.modality, id=modality_id)

    def get_modalities(self):
        """
        Send request to graph api to get all modalities

        Returns:
            Result of request as list of modality objects
        """
        get_response = self.graph_api_service.get_nodes("Modality")
        modalities = [BasicModalityOut(id=modality["id"], modality=modality["properties"][0]["value"])
                      for modality in get_response["nodes"]]

        return ModalitiesOut(modalities=modalities)

    def get_modality(self, modality_id: int):
        """
        Send request to graph api to get given modality

        Args:
        modality_id (int): Id of modality

        Returns:
            Result of request as modality object
        """
        get_response = self.graph_api_service.get_node(modality_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=modality_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Modality":
            return NotFoundByIdModel(id=modality_id, errors="Node not found.")

        modality = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            modality[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(modality_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == modality_id:
                modality['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                 name=relation["name"], relation_id=relation["id"]))
            else:
                modality['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                          name=relation["name"],
                                                                          relation_id=relation["id"]))

        return ModalityOut(**modality)
