from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut
from modality.modality_model import ModalityIn
from modality.modality_service import ModalityService
from live_activity.live_activity_model import LiveActivityIn
from live_activity.live_activity_service import LiveActivityService


class ObservableInformationService:
    """
    Object to handle logic of observable information requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        modality_service (ModalityService): Service used to communicate with Modality
        live_activity_service (LiveActivityService): Service used to communicate with Live Activity
    """
    graph_api_service = GraphApiService()
    modality_service = ModalityService()
    live_activity_service = LiveActivityService()

    def save_observable_information(self, observable_information: ObservableInformationIn):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added

        Returns:
            Result of request as observable information object
        """
        node_response = self.graph_api_service.create_node("`Observable information`")

        if node_response["errors"] is not None:
            return ObservableInformationOut(modality=observable_information.modality,
                                            live_activity=observable_information.live_activity,
                                            errors=node_response["errors"])

        observable_information_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(observable_information_id, observable_information)
        if properties_response["errors"] is not None:
            return ObservableInformationOut(errors=properties_response["errors"])

        modality = ModalityIn(modality=observable_information.modality)
        node_response_modality = self.modality_service.save_modality(modality)
        modality_id = node_response_modality.id
        self.graph_api_service.create_relationships(observable_information_id, modality_id, "hasModality")

        live_activity = LiveActivityIn(live_activity=observable_information.live_activity)
        node_response_live_activity = self.live_activity_service.save_live_activity(live_activity)
        live_activity_id = node_response_live_activity.id
        self.graph_api_service.create_relationships(observable_information_id, live_activity_id, "hasLiveActivity")

        return ObservableInformationOut(modality=observable_information.modality,
                                        live_activity=observable_information.live_activity,
                                        id=observable_information_id)
