from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_data.registered_data_model import RegisteredDataIn, RegisteredDataNodesOut, \
    BasicRegisteredDataOut, RegisteredDataOut
from models.not_found_model import NotFoundByIdModel
from registered_data.registered_data_service import RegisteredDataService


class RegisteredDataServiceGraphDB(RegisteredDataService):
    """
    Object to handle logic of registered data requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.registered_channel_service: RegisteredChannelService = None

    def save_registered_data(self, registered_data: RegisteredDataIn, dataset_name: str):
        """
        Send request to graph api to create new registered data node

        Args:
            registered_data (RegisteredDataIn): Registered data to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as registered data object
        """
        node_response = self.graph_api_service.create_node("Registered Data", dataset_name)

        if node_response["errors"] is not None:
            return RegisteredDataOut(**registered_data.dict(), errors=node_response["errors"])

        registered_data_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(registered_data_id, registered_data,
                                                                       dataset_name)
        if properties_response["errors"] is not None:
            return RegisteredDataOut(**registered_data.dict(), errors=properties_response["errors"])

        return RegisteredDataOut(**registered_data.dict(), id=registered_data_id)

    def get_registered_data_nodes(self, dataset_name: str):
        """
        Send request to graph api to get registered_data_nodes

        Args:
            dataset_name (str): name of dataset

        Returns:
            Result of request as list of registered_data_nodes objects
        """
        get_response = self.graph_api_service.get_nodes("Registered Data", dataset_name)

        registered_data_nodes = []

        for registered_data_node in get_response["nodes"]:
            properties = {'id': registered_data_node['id'], 'additional_properties': []}
            for property in registered_data_node["properties"]:
                if property["key"] == "source":
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            registered_data = BasicRegisteredDataOut(**properties)
            registered_data_nodes.append(registered_data)

        return RegisteredDataNodesOut(registered_data_nodes=registered_data_nodes)

    def get_registered_data(self, registered_data_id: Union[int, str], dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given registered data

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            registered_data_id (int | str): identity of registered data
            dataset_name (str): name of dataset

        Returns:
            Result of request as registered data object
        """
        get_response = self.graph_api_service.get_node(registered_data_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=registered_data_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Registered Data":
            return NotFoundByIdModel(id=registered_data_id, errors="Node not found.")

        registered_data = create_stub_from_response(get_response, properties=['source'])

        if depth != 0:
            registered_data["registered_channels"] = []

            relations_response = self.graph_api_service.get_node_relationships(registered_data_id, dataset_name)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == registered_data_id & relation["name"] == "hasRegisteredData":
                    registered_data["registered_channels"].append(self.registered_channel_service.
                                                                  get_registered_channel(relation["start_node"],
                                                                                         depth - 1))
            return RegisteredDataOut(**registered_data)
        else:
            return BasicRegisteredDataOut(**registered_data)

    def delete_registered_data(self, registered_data_id: Union[int, str], dataset_name: str):
        """
        Send request to graph api to delete given registered data

        Args:
            registered_data_id (int | str): identity of registered data
            dataset_name (str): name of dataset

        Returns:
            Result of request as registered data object
        """
        get_response = self.get_registered_data(registered_data_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(registered_data_id, dataset_name)
        return get_response

    def update_registered_data(self, registered_data_id: Union[int, str], registered_data: RegisteredDataIn,
                               dataset_name: str):
        """
        Send request to graph api to update given registered data

        Args:
            registered_data_id (int | str): identity of registered data
            registered_data (RegisteredDataIn): Properties to update
            dataset_name (str): name of dataset

        Returns:
            Result of request as registered data object
        """
        get_response = self.get_registered_data(registered_data_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(registered_data_id, dataset_name)
        self.graph_api_service.create_properties(registered_data_id, registered_data, dataset_name)

        registered_data_result = {'id': registered_data_id}
        registered_data_result.update(registered_data.dict())

        return BasicRegisteredDataOut(**registered_data_result)
