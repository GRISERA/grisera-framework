from appearance.appearance_service import AppearanceService
from graph_api_service import GraphApiService
from appearance.appearance_model import AppearanceOcclusionIn, AppearanceOcclusionOut, BasicAppearanceOcclusionOut, \
     AppearanceSomatotypeIn, AppearanceSomatotypeOut, BasicAppearanceSomatotypeOut, AppearancesOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class AppearanceServiceGraphDB(AppearanceService):
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
            return AppearanceOcclusionOut(glasses=appearance.glasses, beard=appearance.beard,
                                          moustache=appearance.moustache, errors=node_response["errors"])

        appearance_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(appearance_id, appearance)
        if properties_response["errors"] is not None:
            return AppearanceOcclusionOut(glasses=appearance.glasses, beard=appearance.beard,
                                          moustache=appearance.moustache, errors=properties_response["errors"])

        return AppearanceOcclusionOut(glasses=appearance.glasses, beard=appearance.beard,
                                      moustache=appearance.moustache, id=appearance_id)

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
            return AppearanceSomatotypeOut(ectomorph=appearance.ectomorph, endomorph=appearance.endomorph,
                                           mesomorph=appearance.mesomorph, errors="Scale range not between 1 and 7")

        node_response = self.graph_api_service.create_node("Appearance")

        if node_response["errors"] is not None:
            return AppearanceSomatotypeOut(ectomorph=appearance.ectomorph, endomorph=appearance.endomorph,
                                           mesomorph=appearance.mesomorph, errors=node_response["errors"])

        appearance_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(appearance_id, appearance)
        if properties_response["errors"] is not None:
            return AppearanceSomatotypeOut(ectomorph=appearance.ectomorph, endomorph=appearance.endomorph,
                                           mesomorph=appearance.mesomorph,  errors=properties_response["errors"])

        return AppearanceSomatotypeOut(ectomorph=appearance.ectomorph, endomorph=appearance.endomorph,
                                       mesomorph=appearance.mesomorph, id=appearance_id)

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

        appearance = {'id': appearance_id, 'relations': [], 'reversed_relations': []}
        appearance.update({property["key"]: property["value"] for property in get_response["properties"]})

        relations_response = self.graph_api_service.get_node_relationships(appearance_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == appearance_id:
                appearance["relations"].append(RelationInformation(second_node_id=relation["end_node"],
                                                                   name=relation["name"], relation_id=relation["id"]))
            else:
                appearance["reversed_relations"].append(RelationInformation(second_node_id=relation["start_node"],
                                                                            name=relation["name"],
                                                                            relation_id=relation["id"]))

        return AppearanceOcclusionOut(**appearance) if "glasses" in appearance.keys() \
            else AppearanceSomatotypeOut(**appearance)

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
            properties["id"] = appearance_node["id"]
            appearance = BasicAppearanceOcclusionOut(**properties) if "glasses" in properties.keys() \
                else BasicAppearanceSomatotypeOut(**properties)
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
        get_response = self.get_appearance(appearance_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        self.graph_api_service.delete_node(appearance_id)
        return get_response

    def update_appearance_occlusion(self, appearance_id: int, appearance: AppearanceOcclusionIn):
        """
        Send request to graph api to update given appearance occlusion model

        Args:
            appearance_id (int): Id of appearance
            appearance (AppearanceOcclusionIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        get_response = self.get_appearance(appearance_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        if type(get_response) is AppearanceSomatotypeOut:
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        self.graph_api_service.create_properties(appearance_id, appearance)

        appearance_response = get_response.dict()
        appearance_response.update(appearance)
        return AppearanceOcclusionOut(**appearance_response)

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

            return AppearanceSomatotypeOut(**appearance.dict(), errors="Scale range not between 1 and 7")

        get_response = self.get_appearance(appearance_id)
        if type(get_response) is NotFoundByIdModel:
            return get_response
        if type(get_response) is AppearanceOcclusionOut:
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        self.graph_api_service.create_properties(appearance_id, appearance)

        appearance_response = get_response.dict()
        appearance_response.update(appearance)
        return AppearanceSomatotypeOut(**appearance_response)
