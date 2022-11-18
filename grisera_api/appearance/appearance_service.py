from graph_api_service import GraphApiService
from appearance.appearance_model import AppearanceOcclusionIn, AppearanceOcclusionOut, BasicAppearanceOcclusionOut, \
     AppearanceSomatotypeIn, AppearanceSomatotypeOut, BasicAppearanceSomatotypeOut, AppearancesOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


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
        print("save_appearance_occlusion not implemented yet")

    def save_appearance_somatotype(self, appearance: AppearanceSomatotypeIn):
        """
        Send request to graph api to create new appearance somatotype model

        Args:
            appearance (AppearanceIn): Appearance to be added

        Returns:
            Result of request as appearance state object
        """
        print("save_appearance_somatotype not implemented yet")

    def get_appearance(self, appearance_id: int):
        """
        Send request to graph api to get given appearance

        Args:
            appearance_id (int): Id of appearance

        Returns:
            Result of request as appearance object
        """
        print("get_appearance not implemented yet")

    def get_appearances(self):
        """
        Send request to graph api to get appearances

        Returns:
            Result of request as list of appearances objects
        """
        print("get_appearances not implemented yet")

    def delete_appearance(self, appearance_id: int):
        """
        Send request to graph api to delete given appearance

        Args:
            appearance_id (int): Id of appearance

        Returns:
            Result of request as appearance object
        """
        print("delete_appearance not implemented yet")

    def update_appearance_occlusion(self, appearance_id: int, appearance: AppearanceOcclusionIn):
        """
        Send request to graph api to update given appearance occlusion model

        Args:
            appearance_id (int): Id of appearance
            appearance (AppearanceOcclusionIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        print("update_appearance_occlusion not implemented yet")

    def update_appearance_somatotype(self, appearance_id: int, appearance: AppearanceSomatotypeIn):
        """
        Send request to graph api to update given appearance somatotype model

        Args:
            appearance_id (int): Id of appearance
            appearance (AppearanceSomatotypeIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        print("update_appearance_somatotype not implemented yet")
