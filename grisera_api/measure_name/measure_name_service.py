from graph_api_service import GraphApiService
from measure_name.measure_name_model import MeasureNameIn, MeasureNameOut, MeasureNamesOut, BasicMeasureNameOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class MeasureNameService:
    """
    Abstract class to handle logic of measure name requests

    """

    def save_measure_name(self, measure_name: MeasureNameIn):
        """
        Send request to graph api to create new measure name

        Args:
            measure_name (MeasureNameIn): Measure name to be added

        Returns:
            Result of request as measure name object
        """

        raise Exception("save_measure_name not implemented yet")

    def get_measure_names(self):
        """
        Send request to graph api to get all measure names

        Returns:
            Result of request as list of measure name objects
        """
        raise Exception("get_measure_names not implemented yet")

    def get_measure_name(self, measure_name_id: int):
        """
        Send request to graph api to get given measure name

        Args:
        measure_name_id (int): Id of measure name

        Returns:
            Result of request as measure name object
        """
        raise Exception("get_measure_name not implemented yet")
