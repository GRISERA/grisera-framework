from graph_api_service import GraphApiService
from appearance.appearance_model import AppearanceOcclusionIn, AppearanceOcclusionOut, BasicAppearanceOcclusionOut, \
     AppearanceSomatotypeIn, AppearanceSomatotypeOut, BasicAppearanceSomatotypeOut, AppearancesOut
from models.not_found_model import NotFoundByIdModel


class AppearanceService:
    """
    Object to handle logic of appearance requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_appearance_occlusion(self, appearance: AppearanceOcclusionIn):
        """
        Send request to graph api to create new appearance occlusion model

        Args:
            appearance (AppearanceIn): Appearance to be added

        Returns:
            Result of request as appearance state object
        """
        node_response = self.graph_api_service.create_node("Appearance")

        if node_response["errors"] is not None:
            return AppearanceOcclusionOut(beard=appearance.beard, moustache=appearance.moustache,
                                          errors=node_response["errors"])

        appearance_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(appearance_id, appearance)
        if properties_response["errors"] is not None:
            return AppearanceOcclusionOut(beard=appearance.beard, moustache=appearance.moustache,
                                          errors=properties_response["errors"])

        return AppearanceOcclusionOut(beard=appearance.beard, moustache=appearance.moustache, id=appearance_id)

    def save_appearance_somatotype(self, appearance: AppearanceSomatotypeIn):
        """
        Send request to graph api to create new appearance somatotype model

        Args:
            appearance (AppearanceIn): Appearance to be added

        Returns:
            Result of request as appearance state object
        """

        if not 1 <= appearance.ectomorph <= 7 or not 1 <= appearance.endomorph <= 7 \
                or not 1 <= appearance.mesomorph <= 7:
            return AppearanceSomatotypeOut(glasses=appearance.glasses, ectomorph=appearance.ectomorph,
                                           endomorph=appearance.endomorph, mesomorph=appearance.mesomorph,
                                           errors="Scale range not between 1 and 7")

        node_response = self.graph_api_service.create_node("Appearance")

        if node_response["errors"] is not None:
            return AppearanceSomatotypeOut(glasses=appearance.glasses, ectomorph=appearance.ectomorph,
                                           endomorph=appearance.endomorph, mesomorph=appearance.mesomorph,
                                           errors=node_response["errors"])

        appearance_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(appearance_id, appearance)
        if properties_response["errors"] is not None:
            return AppearanceSomatotypeOut(glasses=appearance.glasses, ectomorph=appearance.ectomorph,
                                           endomorph=appearance.endomorph, mesomorph=appearance.mesomorph,
                                           errors=properties_response["errors"])

        return AppearanceSomatotypeOut(glasses=appearance.glasses, ectomorph=appearance.ectomorph,
                                       endomorph=appearance.endomorph, mesomorph=appearance.mesomorph, id=appearance_id)

    def get_appearance(self, appearance_id: int):
        """
        Send request to graph api to get given appearance

        Args:
            appearance_id (int): Id of appearance

        Returns:
            Result of request as appearance object
        """
        get_response = self.graph_api_service.get_node(appearance_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=appearance_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Appearance":
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        properties = {property["key"]: property["value"] for property in get_response["properties"]}

        return AppearanceSomatotypeOut(id=appearance_id, glasses=properties["glasses"],
                                       ectomorph=properties["ectomorph"], endomorph=properties["endomorph"],
                                       mesomorph=properties["mesomorph"]) if "glasses" in properties.keys() else \
            AppearanceOcclusionOut(id=appearance_id, beard=properties["beard"], moustache=properties["moustache"])

    def get_appearances(self):
        """
        Send request to graph api to get appearances

        Returns:
            Result of request as list of appearances objects
        """
        get_response = self.graph_api_service.get_nodes("Appearance")

        appearances = []

        for appearance_node in get_response["nodes"]:
            properties = {property["key"]: property["value"] for property in appearance_node["properties"]}
            appearance = BasicAppearanceSomatotypeOut(id=appearance_node["id"], glasses=properties["glasses"],
                                                      ectomorph=properties["ectomorph"], endomorph=
                                                      properties["endomorph"], mesomorph=properties["mesomorph"]) \
                if "glasses" in properties.keys() else BasicAppearanceOcclusionOut(id=appearance_node["id"],
                                                                                   beard=properties["beard"],
                                                                                   moustache=properties["moustache"])
            appearances.append(appearance)

        return AppearancesOut(appearances=appearances)

    def delete_appearance(self, appearance_id: int):
        """
        Send request to graph api to delete given appearance

        Args:
            appearance_id (int): Id of appearance

        Returns:
            Result of request as appearance object
        """
        get_response = self.graph_api_service.get_node(appearance_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=appearance_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Appearance":
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        delete_response = self.graph_api_service.delete_node(appearance_id)

        properties = {property["key"]: property["value"] for property in delete_response["properties"]}

        return AppearanceSomatotypeOut(id=appearance_id, glasses=properties["glasses"],
                                       ectomorph=properties["ectomorph"], endomorph=properties["endomorph"],
                                       mesomorph=properties["mesomorph"]) if "glasses" in properties.keys() else \
            AppearanceOcclusionOut(id=appearance_id, beard=properties["beard"], moustache=properties["moustache"])

    def update_appearance_occlusion(self, appearance_id: int, appearance: AppearanceOcclusionIn):
        """
        Send request to graph api to update given appearance occlusion model

        Args:
            appearance_id (int): Id of appearance
            appearance (AppearanceOcclusionIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        get_response = self.graph_api_service.get_node(appearance_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=appearance_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Appearance" or \
                get_response["properties"][0]["key"] not in ["beard", "moustache"]:
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        self.graph_api_service.create_properties(appearance_id, appearance)

        return AppearanceOcclusionOut(id=appearance_id, beard=appearance.beard, moustache=appearance.moustache)

    def update_appearance_somatotype(self, appearance_id: int, appearance: AppearanceSomatotypeIn):
        """
        Send request to graph api to update given appearance somatotype model

        Args:
            appearance_id (int): Id of appearance
            appearance (AppearanceSomatotypeIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        if not 1 <= appearance.ectomorph <= 7 or not 1 <= appearance.endomorph <= 7 \
                or not 1 <= appearance.mesomorph <= 7:
            return AppearanceSomatotypeOut(glasses=appearance.glasses, ectomorph=appearance.ectomorph,
                                           endomorph=appearance.endomorph, mesomorph=appearance.mesomorph,
                                           errors="Scale range not between 1 and 7")

        get_response = self.graph_api_service.get_node(appearance_id)
        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=appearance_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Appearance" or \
                get_response["properties"][0]["key"] in ["beard", "moustache"]:
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        self.graph_api_service.create_properties(appearance_id, appearance)

        return AppearanceSomatotypeOut(id=appearance_id, glasses=appearance.glasses, ectomorph=appearance.ectomorph,
                                       endomorph=appearance.endomorph, mesomorph=appearance.mesomorph)
