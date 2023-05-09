from typing import Union
from bson import ObjectId
from mongo_service.collection_mapping import Collections
from mongo_service.service_mixins import GenericMongoServiceMixin
from observable_information.observable_information_model import (
    ObservableInformationIn,
    ObservableInformationOut,
    BasicObservableInformationOut,
    ObservableInformationsOut,
)
from observable_information.observable_information_service import (
    ObservableInformationService,
)
from models.not_found_model import NotFoundByIdModel


class ObservableInformationServiceMongoDB(
    ObservableInformationService, GenericMongoServiceMixin
):
    """
    Object to handle logic of observable information requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    modality_service (ModalityService): Service used to communicate with Modality
    life_activity_service (LifeActivityService): Service used to communicate with Life Activity
    recording_service (RecordingService): Service used to communicate with Recording
    """

    def __init__(self):
        super().__init__()
        self.model_out_class = ObservableInformationOut
        self.recording_service = None
        self.life_activity_service = None
        self.modality_service = None
        self.time_series_service = None

    def save_observable_information(
        self, observable_information: ObservableInformationIn
    ):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added.
            recording_id here is required

        Returns:
            Result of request as observable information object
        """

        related_recording = self.recording_service.get_recording(
            observable_information.recording_id
        )
        related_recording_exists = type(related_recording) is not NotFoundByIdModel
        if not related_recording_exists:
            return ObservableInformationOut(
                errors={"errors": "given recording does not exist"}
            )

        related_modality = self.modality_service.get_modality(
            observable_information.modality_id
        )
        related_modality_exists = related_modality is not NotFoundByIdModel
        if (
            observable_information.modality_id is not None
            and not related_modality_exists
        ):
            return ObservableInformationOut(
                errors={"errors": "given modality does not exist"}
            )

        related_life_activity = self.life_activity_service.get_life_activity(
            observable_information.life_activity_id
        )
        related_life_activity_exists = related_life_activity is not NotFoundByIdModel
        if (
            observable_information.life_activity_id is not None
            and not related_life_activity_exists
        ):
            return ObservableInformationOut(
                errors={"errors": "given life activity does not exist"}
            )

        return self.recording_service.add_observable_information(observable_information)

    def get_multiple(
        self, query: dict = {}, depth: int = 0, source: str = "", *args, **kwargs
    ):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of dictionaries
        """
        recording_query = {
            f"{Collections.OBSERVABLE_INFORMATION}.{field}": value
            for field, value in query
        }
        recording_result = self.recording_service.get_multiple(
            recording_query,
            depth=depth - 1,
            source=Collections.OBSERVABLE_INFORMATION,
            projection=self._get_recording_projection(query),
        )

        result = []
        for recording_result in recording_result:
            observable_informations = recording_result["observable_informations"]
            del recording_result["observable_informations"]
            for observable_information in observable_informations:
                self._add_related_documents(
                    observable_information,
                    depth - 1,
                    source,
                    recording_result,
                )
            result += observable_informations

        return result

    def get_observable_informations(self):
        """
        Send request to graph api to get observable information
        Returns:
            Result of request as list of observable information objects
        """
        observable_information_dicts = self.get_multiple()
        results = [
            BasicObservableInformationOut(**result)
            for result in observable_information_dicts
        ]
        return ObservableInformationsOut(observable_informations=results)

    def get_single_dict(
        self, id: Union[str, int], depth: int = 0, source: str = "", *args, **kwargs
    ):
        observable_information_objectid = ObjectId(observable_information_objectid)
        recording_result = self.recording_service.get_multiple(
            {
                f"{Collections.OBSERVABLE_INFORMATION}.id": observable_information_objectid
            },
            depth=depth - 1,
            source=Collections.OBSERVABLE_INFORMATION,
            projection=self._get_recording_projection(
                {"id": observable_information_objectid}
            ),
        )
        if (
            len(recording_result) == 0
            or len(recording_result[0][Collections.OBSERVABLE_INFORMATION]) == 0
        ):
            return NotFoundByIdModel(
                id=id,
                errors={"errors": "observable information not found"},
            )
        related_recording = recording_result[0]
        observable_information_dict = related_recording[
            Collections.OBSERVABLE_INFORMATION
        ][0]
        del related_recording[Collections.OBSERVABLE_INFORMATION]
        self._add_related_documents(
            observable_information_dict, depth, source, related_recording
        )
        return observable_information_dict

    def get_single(
        self, id: Union[str, int], depth: int = 0, source: str = "", *args, **kwargs
    ):
        result = self.get_single_dict(id, depth, source, *args, **kwargs)
        if type(result) is NotFoundByIdModel:
            return result
        return ObservableInformationOut(**result)

    def get_observable_information(
        self,
        observable_information_id: Union[str, int],
        depth: int = 0,
        source: str = "",
    ):
        """
        Send request to graph api to get given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        return self.get_single(observable_information_id, depth, source)

    def delete_observable_information(self, observable_information_id: Union[str, int]):
        """
        Send request to graph api to delete given observable information. Removal is performed by recording service, as observable information
        is embeded within recording
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        observable_information = self.get_observable_information(
            observable_information_id
        )
        if type(observable_information) is NotFoundByIdModel:
            return NotFoundByIdModel(
                id=observable_information_id,
                errors={"errors": "observable information not found"},
            )
        return self.recording_service.remove_observable_information(
            observable_information
        )

    def update_observable_information_relationships(
        self,
        observable_information_id: Union[str, int],
        observable_information: BasicObservableInformationOut,
    ):
        """
        Send request to graph api to update given observable information
        Args:
            observable_information_id (int): Id of observable information
            observable_information (ObservableInformationIn): Relationships to update
        Returns:
            Result of request as observable information object
        """
        return self.recording_service.update_observable_information(
            observable_information.dict()
        )

    def _add_related_documents(
        self,
        observable_information: dict,
        depth: int,
        source: str,
        recording: dict,
    ):
        """Recording is taken from previous get query"""
        if depth > 0:
            self._add_related_time_series(observable_information, depth, source)
            self._add_related_modalities(observable_information, depth, source)
            self._add_related_life_activities(observable_information, depth, source)
            self._add_recording(observable_information, depth, source, recording)

    def _add_recording(
        self, observable_information: dict, depth: int, source: str, recording: dict
    ):
        """Recording has already added related documents"""
        if source != "recording":
            observable_information["recording"] = recording

    def _add_related_modalities(
        self, observable_information: dict, depth: int, source: str
    ):
        pass
        # TODO add when modalities service is ready

    def _add_related_life_activities(
        self, observable_information: dict, depth: int, source: str
    ):
        pass
        # TODO add when life_activities service is ready

    def _add_related_time_series(
        self, observable_information: dict, depth: int, source: str
    ):
        pass
        # TODO add when time series service is ready

    @staticmethod
    def _get_recording_projection(query):
        return {
            Collections.OBSERVABLE_INFORMATION: {"$elemMatch": query},
            "additional_properties": 1,
            "participation_id": 1,
            "registered_channel_id": 1,
        }
