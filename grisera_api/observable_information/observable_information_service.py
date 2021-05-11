from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut


class ObservableInformationService:
    """
    Object to handle logic of observable information requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

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

        return ObservableInformationOut(modality=observable_information.modality,
                                        live_activity=observable_information.live_activity,
                                        id=observable_information_id)
