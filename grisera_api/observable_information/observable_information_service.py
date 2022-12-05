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
    Abstract class to handle logic of observable information requests

    """

    def save_observable_information(self, observable_information: ObservableInformationIn):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added

        Returns:
            Result of request as observable information object
        """
        raise Exception("save_observable_information not implemented yet")

    def get_observable_informations(self):
        """
        Send request to graph api to get observable information
        Returns:
            Result of request as list of observable information objects
        """
        raise Exception("get_observable_informations not implemented yet")

    def get_observable_information(self, observable_information_id: int):
        """
        Send request to graph api to get given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        raise Exception("get_observable_information not implemented yet")

    def delete_observable_information(self, observable_information_id: int):
        """
        Send request to graph api to delete given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        raise Exception("delete_observable_information not implemented yet")

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
        raise Exception("update_observable_information_relationships not implemented yet")
