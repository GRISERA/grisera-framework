from graph_api_service import GraphApiService
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, ArrangementsOut, BasicArrangementOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ArrangementService:
    """
    Abstract class to handle logic of arrangement requests

    """

    def save_arrangement(self, arrangement: ArrangementIn):
        """
        Send request to graph api to create new arrangement

        Args:
            arrangement (ArrangementIn): Arrangement to be added

        Returns:
            Result of request as arrangement object
        """
        raise Exception("save_arrangement not implemented yet")

    def get_arrangements(self):
        """
        Send request to graph api to get all arrangements

        Returns:
            Result of request as list of arrangement objects
        """
        raise Exception("get_arrangements not implemented yet")

    def get_arrangement(self, arrangement_id: int):
        """
        Send request to graph api to get given arrangement

        Args:
            arrangement_id (int): Id of arrangement

        Returns:
            Result of request as arrangement object
        """
        raise Exception("get_arrangement not implemented yet")

    def delete_arrangement(self, arrangement_id: int):
        """
        Send request to graph api to get given arrangement
        Args:
            arrangement_id (int): Id of arrangement
        Returns:
            Result of request as arrangement object
        """
        raise Exception("Reference to an abstract class.")

    def update_arrangement(self, arrangement_id: int, arrangement: ArrangementIn):
        """
        Send request to graph api to update given arrangement
        Args:
            arrangement_id (int): Id of arrangement
            arrangement (ArrangementIn): Arrangement to be updated
        Returns:
            Result of request as arrangement object
        """
        raise Exception("Reference to an abstract class.")
