import requests
import json
from pydantic import BaseModel

from graph_api_config import graph_api_address


class GraphApiService:
    """
    Object that handles communication with graph api

    Attributes:
        graph_api_url (str): Graph API URL
    """
    graph_api_url = graph_api_address

    def add_database_name_to_url(self, database_name):
        url = "?database_name=" + database_name
        return url

    def post(self, url_part, request_body, database_name: str):
        """
        Send request post to Graph API

        Args:
            url_part (str): Part to add at the end of url
            request_body (dict): Body of request

        Returns:
            Result of request
        """


        url_part += self.add_database_name_to_url(database_name)
        print("###### URL_PART: ", url_part)
        response = requests.post(url=self.graph_api_url + url_part,
                                 json=request_body).json()
        print("###### RESPONSE: ", response)
        # print("###### RESPONSE: ", response)
        # try:
        #     response_data = response.json()
        # except json.JSONDecodeError as json_error:
        #     print(f"JSON decoding error occurred: {json_error}")
        #     # Handle the JSONDecodeError
        #     response_data = {}

        return response

    def get(self, url_part, params, database_name: str):
        """
        Send request get to Graph API

        Args:
            url_part (str): Part to add at the end of url
            params (dict): Parameters of request

        Returns:
            Result of request
        """
        url_part += self.add_database_name_to_url(database_name)
        response = requests.get(url=self.graph_api_url + url_part,
                                params=params).json()
        return response

    def delete(self, url_part, params, database_name: str):
        """
        Send request get to Graph API

        Args:
            url_part (str): Part to add at the end of url
            params (dict): Parameters of request

        Returns:
            Result of request
        """
        url_part += self.add_database_name_to_url(database_name)
        response = requests.delete(url=self.graph_api_url + url_part,
                                   params=params).json()
        return response

    def create_node(self, label: str, database_name: str):
        """
        Send to the Graph API request to create a node

        Args:
            label (str): Label for node
        Returns:
            Result of request
        """
        print("LABEL: ", label)
        #request_body = {"labels": [label], "database_name": database_name}
        request_body = {"labels": [label], "database_name": [database_name]}
        print("LABEL DISCTIONARY", request_body)
        return self.post("/nodes", request_body, database_name)

    def get_nodes(self, label: str, database_name: str):
        """
        Send to the Graph API request to get nodes with given label

        Args:
            label (str): Label of nodes
        Returns:
            Result of request
        """
        request_params = {"label": label, "database_name": database_name}
        return self.get("/nodes", request_params, database_name)

    def get_node(self, id: int, database_name: str):
        """
        Send to the Graph API request to get node with given id

        Args:
            id (int): ID of node
        Returns:
            Result of request
        """
        request_params = {"database_name": database_name}
        return self.get("/nodes/"+str(id), request_params, database_name)

    def get_node_relationships(self, node_id: int, database_name: str):
        """
        Send to the Graph API request to get node's relationship

        Args:
            node_id (int): Id of node
        Returns:
            Result of request
        """
        request_params = {"database_name": database_name}
        return self.get(f"/nodes/{node_id}/relationships", request_params, database_name)

    def get_nodes_by_query(self, query, database_name: str):
        """
        Send to the Graph API request to get nodes with given label
        Args:
            query (): Query
        Returns:
            Result of request
        """
        return self.post("/nodes_query", query, database_name)

    def delete_node(self, node_id: int, database_name: str):
        """
        Send to the Graph API request to delete node

        Args:
            node_id (int): Id of node
        Returns:
            Result of request
        """
        request_params = {"database_name": database_name}
        return self.delete(f"/nodes/{node_id}", request_params, database_name)

    def delete_node_properties(self, node_id: int, database_name: str):
        """
        Send to the Graph API request to delete node properties

        Args:
            node_id (int): Id of node
        Returns:
            Result of request
        """
        request_params = {"database_name": database_name}
        return self.delete(f"/nodes/{node_id}/properties", request_params, database_name)

    def create_properties(self, node_id: int, node_model: BaseModel, database_name: str):
        """
        Send to the Graph API request to create properties for given node

        Args:
            node_id (int): Id of node for which properties will be added
            node_model (BaseModel): Model of node with properties to add

        Returns:
            Result of request
        """
        node_dict = node_model.dict()
        request_body = []
        for key, value in node_dict.items():
            if key == 'additional_properties' and value is not None:
                request_body.extend(self.create_additional_properties(property_dict=node_dict))
            elif value is not None and not isinstance(value, list) and not isinstance(value, dict):
                request_body.append({"key": key, "value": value, "database_name": database_name})

        return self.post("/nodes/{}/properties".format(node_id), request_body, database_name)

    def create_relationships(self, start_node: int, end_node: int, name: str, database_name: str):
        """
        Send to the Graph API request to create a relationship

        Args:
            start_node(int): Id of node which starts connection
            end_node(int): Id of node which ends connection
            name(str): Name of the relationship

        Returns:
            Result of request
       """
        request_body = {"start_node": start_node, "end_node": end_node, "name": name, "database_name": [database_name]}
        return self.post("/relationships", request_body, database_name)

    def delete_relationship(self, relationship_id: int, database_name: str):
        """
        Send to the Graph API request to delete relationship

        Args:
            relationship_id (int): Id of relationship
        Returns:
            Result of request
        """
        request_params = {"database_name": database_name}
        return self.delete(f"/relationships/{relationship_id}", request_params, database_name)

    def create_additional_properties(self, property_dict: dict):
        """
        Creates request body for additional properties

        Args:
            property_dict (dict): dictionary of properties

        Returns:
            Request body
        """
        return [{"key": additional_properties['key'], "value": additional_properties['value']}
                for additional_properties in property_dict['additional_properties']]
