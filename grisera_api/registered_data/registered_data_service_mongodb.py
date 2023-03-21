from registered_data.registered_data_model import (
    RegisteredDataIn,
    RegisteredDataNodesOut,
    BasicRegisteredDataOut,
    RegisteredDataOut,
)
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from registered_data.registered_data_service import RegisteredDataService
from mongo_service import mongo_api_service


class RegisteredDataServiceMongoDB(RegisteredDataService):
    """
    Object to handle logic of registered data requests
    """

    def __init__(self, registered_channel_service):
        self.registered_channel_service = registered_channel_service

    def save_registered_data(self, registered_data: RegisteredDataIn):
        """
        Send request to mongo api to create new registered data node

        Args:
            registered_data (RegisteredDataIn): Registered data to be added

        Returns:
            Result of request as registered data object
        """
        registered_data_id = mongo_api_service.create_document(registered_data)

        return self.get_registered_data(registered_data_id)

    def get_registered_data_nodes(self):
        """
        Send request to mongo api to get ass registered data nodes

        Args:
            query (dict): Query for mongo request.

        Returns:
            Result of request as list of registered data objects
        """
        registed_data = mongo_api_service.get_documents(BasicRegisteredDataOut)
        result = [BasicRegisteredDataOut(**rd) for rd in registed_data]

        return RegisteredDataNodesOut(registered_data_nodes=result)

    def get_registered_data(self, registered_data_id: int):
        """
        Send request to graph api to get given registered data

        Args:
            registered_channel_id (int): Id of registered data

        Returns:
            Result of request as registered data object
        """
        registered_data = self.get_registered_data_traverse(registered_data_id, 0, "")
        if registered_data is NotFoundByIdModel:
            return registered_data
        return RegisteredDataOut(**registered_data)

    def get_registered_data_traverse(
        self, registered_data_id: int, depth: int, source: str
    ):
        """
        Send request to graph api to get given registered data with related models

        Args:
            registered_channel_id (int): Id of registered data
            depth (int): this attribute specifies how many models will be traversed to create the response.
                         for depth=0, only no further models will be travesed.
            source (str): internal argument for mongo services, used to tell the direction of model fetching.

        Returns:
            Result of request as registered data dictionary
        """
        registered_data = mongo_api_service.get_document(
            registered_data_id, RegisteredDataOut
        )

        if registered_data is NotFoundByIdModel:
            return registered_data

        self._add_related_registered_channels(registered_data, depth, source)

        return RegisteredDataOut(**registered_data)

    def delete_registered_data(self, registered_data_id: int):
        """
        Send request to mongo api to delete given registered data

        Args:
        registered_data_id (int): Id of registered data

        Returns:
            Result of request as registered data object
        """
        registered_data = self.get_registered_data(registered_data_id)

        if registered_data is None:
            return NotFoundByIdModel(
                id=registered_data_id,
                errors={"errors": "registered data not found"},
            )

        mongo_api_service.delete_document(registered_data)
        return registered_data

    def update_registered_data(
        self, registered_data_id: int, registered_data: RegisteredDataIn
    ):
        """
        Send request to mongo api to update given registered data

        Args:
        registered_data_id (int): Id of registered data
        registered_data (RegisteredDataIn): Properties to update

        Returns:
            Result of request as registered data object
        """
        get_response = self.get_registered_data(registered_data_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        mongo_api_service.update_document(registered_data_id, registered_data)

        return self.get_registered_data(registered_data_id)

    def _add_related_registered_channels(
        self, registered_data: dict, depth: int, source: str
    ):
        if source != "recording" and depth > 0:
            registered_data[
                "registered_channels"
            ] = self.registered_channel_service.get_registered_channels_traverse(
                {"registered_data_id": registered_data["id"]},
                depth=depth - 1,
                source="registered_data",
            )
