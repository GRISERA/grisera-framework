import requests
from graph_api_config import graph_api_address
from pydantic import BaseModel


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
                for dict_property in node_dict[key]:
                    keys = list(dict_property.keys())
                    values = list(dict_property.values())
                    for k, v in zip(keys, values):
                        request_body.append({"key": k, "value": v})
            elif isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, list) and k == 'additional_properties':
                        [request_body.append(
                            {"key": additional_properties['key'], "value": additional_properties['value']})
                         for additional_properties in v]
                    else:
                        request_body.append({"key": k, "value": v})
            elif isinstance(value, list) and key == 'additional_properties':
                [request_body.append({"key": additional_properties['key'], "value": additional_properties['value']})
                 for additional_properties in value]
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
