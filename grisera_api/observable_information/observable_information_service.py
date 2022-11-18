from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut, \
    BasicObservableInformationOut, ObservableInformationsOut
from modality.modality_service import ModalityService
from life_activity.life_activity_service import LifeActivityService
from recording.recording_service import RecordingService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ObservableInformationService:
    """
    Object to handle logic of observable information requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    modality_service (ModalityService): Service used to communicate with Modality
    life_activity_service (LifeActivityService): Service used to communicate with Life Activity
    recording_service (RecordingService): Service used to communicate with Recording
    """
    graph_api_service = GraphApiService()
    modality_service = ModalityService()
    life_activity_service = LifeActivityService()
    recording_service = RecordingService()

    def save_observable_information(self, observable_information: ObservableInformationIn):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added

        Returns:
            Result of request as observable information object
        """
        print("save_observable_information not implemented yet")

    def get_observable_informations(self):
        """
        Send request to graph api to get observable information
        Returns:
            Result of request as list of observable information objects
        """
        print("get_observable_informations not implemented yet")

    def get_observable_information(self, observable_information_id: int):
        """
        Send request to graph api to get given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        print("get_observable_information not implemented yet")

    def delete_observable_information(self, observable_information_id: int):
        """
        Send request to graph api to delete given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        print("delete_observable_information not implemented yet")

    def update_observable_information_relationships(self, observable_information_id: int,
                                                    observable_information: ObservableInformationIn):
        """
        Send request to graph api to update given observable information
        Args:
            observable_information_id (int): Id of observable information
            observable_information (ObservableInformationIn): Relationships to update
        Returns:
            Result of request as observable information object
        """
        print("update_observable_information_relationships not implemented yet")
