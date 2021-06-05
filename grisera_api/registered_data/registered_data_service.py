from graph_api_service import GraphApiService
from registered_data.registered_data_model import RegisteredDataIn, RegisteredDataOut


class RegisteredDataService:
    """
    Object to handle logic of registered data requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_registered_data(self, registered_data: RegisteredDataIn):
        """
        Send request to graph api to create new registered data node

        Args:
            registered_data (RegisteredDataIn): Registered data to be added

        Returns:
            Result of request as registered data object
        """
        node_response = self.graph_api_service.create_node("`Registered data`")

        if node_response["errors"] is not None:
            return RegisteredDataOut(source=registered_data.source, errors=node_response["errors"])

        registered_data_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(registered_data_id, registered_data)
        if properties_response["errors"] is not None:
            return RegisteredDataOut(source=registered_data.source, errors=properties_response["errors"])

        return RegisteredDataOut(source=registered_data.source, id=registered_data_id,
                                 additional_properties=registered_data.additional_properties)
