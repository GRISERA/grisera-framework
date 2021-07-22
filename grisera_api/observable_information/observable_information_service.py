from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut
from modality.modality_service import ModalityService
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

        modalities = self.modality_service.get_modalities().modalities
        modality_id = next(modality.id for modality in modalities
                           if modality.modality == observable_information.modality)
        self.graph_api_service.create_relationships(observable_information_id, modality_id, "hasModality")

        live_activities = self.live_activity_service.get_live_activities().live_activities
        live_activity_id = next(live_activity.id for live_activity in live_activities if
                                observable_information.live_activity == live_activity.live_activity)
        self.graph_api_service.create_relationships(observable_information_id, live_activity_id, "hasLiveActivity")

        return ObservableInformationOut(modality=observable_information.modality,
                                        live_activity=observable_information.live_activity,
                                        id=observable_information_id)
