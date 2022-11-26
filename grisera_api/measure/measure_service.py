from graph_api_service import GraphApiService
from measure.measure_model import MeasurePropertyIn, BasicMeasureOut, \
    MeasuresOut, MeasureOut, MeasureIn, MeasureRelationIn
from measure_name.measure_name_service import MeasureNameService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class MeasureService:
    """
    Abstract class to handle logic of measure requests

    """

    def save_measure(self, measure: MeasureIn):
        """
        Send request to graph api to create new measure

        Args:
            measure (MeasureIn): Measure to be added

        Returns:
            Result of request as measure object
        """
        raise Exception("save_measure not implemented yet")

    def get_measures(self):
        """
        Send request to graph api to get measures

        Returns:
            Result of request as list of measures objects
        """
        raise Exception("get_measures not implemented yet")

    def get_measure(self, measure_id: int):
        """
        Send request to graph api to get given measure

        Args:
            measure_id (int): Id of measure

        Returns:
            Result of request as measure object
        """
        raise Exception("get_measure not implemented yet")

    def delete_measure(self, measure_id: int):
        """
        Send request to graph api to delete given measure

        Args:
            measure_id (int): Id of measure

        Returns:
            Result of request as measure object
        """
        raise Exception("delete_measure not implemented yet")

    def update_measure(self, measure_id: int, measure: MeasurePropertyIn):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int): Id of measure
            measure (MeasurePropertyIn): Properties to update

        Returns:
            Result of request as measure object
        """
        raise Exception("update_measure not implemented yet")

    def update_measure_relationships(self, measure_id: int,
                                     measure: MeasureRelationIn):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int): Id of measure
            measure (MeasureRelationIn): Relationships to update

        Returns:
            Result of request as measure object
        """
        raise Exception("update_measure_relationships not implemented yet")
