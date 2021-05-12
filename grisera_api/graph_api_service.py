import requests
from graph_api_config import graph_api_address
from pydantic import BaseModel


def create_additional_properties(property_dict: dict):
    """
    Creates request body for additional properties

    Args:
        property_dict (dict): dictionary of properties

    Returns:
        Request body
    """
    request_body = [{"key": additional_properties['key'], "value": additional_properties['value']}
                    for additional_properties in property_dict['additional_properties']]

    return request_body


def create_properties_from_dict(dictionary: dict):
    """
    Creates request body from dictionary with properties

    Args:
        dictionary (dict): dictionary of properties

    Returns:
        Request body
    """
    request_body = []
    for k, v in dictionary.items():
        if isinstance(v, list) and k == 'additional_properties':
            request_body.extend(create_additional_properties(property_dict=dictionary))
        elif isinstance(v, list) and k != 'additional_properties':
            request_body.extend(create_properties_from_list_of_dict(list_of_dicts=v))
        else:
            request_body.append({"key": k, "value": v})
    return request_body


def create_properties_from_list_of_dict(list_of_dicts: list):
    """
    Creates request body from list of dictionaries with properties

    Args:
        list_of_dicts (list): list of dictionaries of properties

    Returns:
        Request body
    """
    request_body = []
    for dict_property in list_of_dicts:
        request_body.extend(create_properties_from_dict(dict_property))

    return request_body


class GraphApiService:
    """
    Object that handles communication with graph api

    Attributes:
        graph_api_url (str): Graph API URL
    """
    graph_api_url = graph_api_address

    def post(self, url_part, request_body):
        """
        Send request post to Graph API

        Args:
            url_part (str): Part to add at the end of url
            request_body (dict): Body of request

        Returns:
            Result of request
        """

        response = requests.post(url=self.graph_api_url + url_part,
                                 json=request_body).json()
        return response

    def create_node(self, label: str):
        """
        Send to the Graph API request to create a node

        Args:
            label (str): Label for node
        Returns:
            Result of request
        """
        request_body = {"labels": [label]}
        return self.post("/nodes", request_body)

    def create_properties(self, node_id: int, node_model: BaseModel):
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
            if isinstance(value, list) and key != 'additional_properties':
                request_body.extend(create_properties_from_list_of_dict(list_of_dicts=value))
            elif isinstance(value, dict):
                request_body.extend(create_properties_from_dict(dictionary=value))
            elif isinstance(value, list) and key == 'additional_properties':
                request_body.extend(create_additional_properties(property_dict=node_dict))
            else:
                request_body.append({"key": key, "value": value})

        return self.post("/nodes/{}/properties".format(node_id), request_body)

    def create_relationships(self, start_node: int, end_node: int, name: str):
        """
        Send to the Graph API request to create a relationship

        Args:
            start_node(int): Id of node which starts connection
            end_node(int): Id of node which ends connection
            name(str): Name of the relationship

        Returns:
            Result of request
       """
        request_body = {"start_node": start_node, "end_node": end_node, "name": name}
        return self.post("/relationships", request_body)
