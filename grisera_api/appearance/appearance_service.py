from graph_api_service import GraphApiService
from appearance.appearance_model import AppearanceOcclusionIn, AppearanceOcclusionOut, \
    AppearanceSomatotypeIn, AppearanceSomatotypeOut


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
