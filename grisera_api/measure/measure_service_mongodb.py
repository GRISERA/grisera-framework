from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from measure.measure_model import (
    MeasurePropertyIn,
    BasicMeasureOut,
    MeasuresOut,
    MeasureOut,
    MeasureIn,
    MeasureRelationIn,
)
from measure.measure_service import MeasureService
from measure_name.measure_name_service import MeasureNameService
from models.not_found_model import NotFoundByIdModel
from mongo_service.mongo_api_service import MongoApiService
from mongo_service.service_mixins import GenericMongoServiceMixin
from time_series.time_series_service import TimeSeriesService


class MeasureServiceMongoDB(MeasureService, GenericMongoServiceMixin):
    """
    Object to handle logic of measure requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_name_service (MeasureNameService): Service to manage measure name models
    """

    def __init__(self):
        super().__init__()
        self.mongo_api_service = MongoApiService()
        self.model_out_class = MeasureOut
        self.time_series_service = None
        self.measure_name_service = None

    def save_measure(self, measure: MeasureIn):
        """
        Send request to mongo api to create new measure

        Args:
            measure (MeasureIn): Measure to be added

        Returns:
            Result of request as measure object
        """
        related_mn = self.measure_name_service.get_measure_name(measure.measure_name_id)
        mn_exists = related_mn is not NotFoundByIdModel
        if measure.measure_name_id is not None and not mn_exists:
            return MeasureOut(errors={"errors": "given measure name does not exist"})

        return self.create(measure)

    def get_measures(self, query: dict = {}):
        """
        Send request to mongo api to get measures

        Args:
            query (dict): query for filtering measures

        Returns:
            Result of request as list of measures objects
        """
        measures_dict = self.get_multiple(query)
        results = [BasicMeasureOut(**result) for result in measures_dict]
        return MeasuresOut(measures=results)

    def get_measure(
        self, measure_id: Union[int, str], depth: int = 0, source: str = ""
    ):
        """
        Send request to mongo api to get given measure

        Args:
            measure_id (int | str): identity of measure
            depth: (int): specifies how many related entities will be traversed to create the response
            source (str): internal argument for mongo services, used to tell the direction of model fetching.

        Returns:
            Result of request as measure object
        """
        return self.get_single(measure_id, depth, source)

    def delete_measure(self, measure_id: Union[int, str]):
        """
        Send request to mongo api to delete given measure

        Args:
            measure_id (int | str): identity of measure

        Returns:
            Result of request as measure object
        """
        return self.delete(measure_id)

    def update_measure(self, measure_id: Union[int, str], measure: MeasurePropertyIn):
        """
        Send request to mongo api to update given measure

        Args:
            measure_id (int | str): identity of measure
            measure (MeasurePropertyIn): Properties to update

        Returns:
            Result of request as measure object
        """
        existing_measure = self.get_measure(measure_id)
        for field, value in measure.dict().items:
            setattr(existing_measure, field, value)

        self.mongo_api_service.update_document(
            measure_id,
            existing_measure,
        )
        return existing_measure

    def update_measure_relationships(
        self, measure_id: Union[int, str], measure: MeasureRelationIn
    ):
        """
        Send request to mongo api to update given measure

        Args:
            measure_id (int | str): identity of measure
            measure (MeasureRelationIn): Relationships to update

        Returns:
            Result of request as measure object
        """
        existing_measure = self.get_measure(measure_id)

        if type(existing_measure) is NotFoundByIdModel:
            return existing_measure

        related_mn = self.measure_name_service.get_measure_name(measure.measure_name_id)
        mn_exists = related_mn is not NotFoundByIdModel
        if measure.measure_name_id is not None and not mn_exists:
            return MeasureOut(errors={"errors": "given measure name does not exist"})

        existing_measure.measure_name_id = measure.measure_name_id

        self.mongo_api_service.update_document(
            measure_id,
            existing_measure,
        )
        return existing_measure
