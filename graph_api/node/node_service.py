import requests
import string
from requests.auth import HTTPBasicAuth
from database_config import database
from node.node_model import NodeIn, NodeOut
from property.property_model import PropertyIn
from typing import List


class NodeService:
    """
    Object to handle logic of nodes requests

    Attributes:
        database_url (str): URL to used database
        database_auth (HTTPBasicAuth): Used to authenticate to database
    """
    database_url = (database["address"] + database["commit_path"]) \
        .replace("{database_name}", database["name"])
    database_auth = HTTPBasicAuth(database["user"], database["passwd"])

    def node_exists(self, node_id):
        """
        Check if node exists in the database

        Args:
            node_id(int): id of the node

        Returns:
            True - If there is a node in the database.
            False - If there is not a node in the database.
        """
        check_node_statement = f"MATCH (n) where id(n) ={node_id} return n"

        commit_body = {
            "statements": [{"statement": check_node_statement}]
        }
        response = requests.post(url=self.database_url,
                                 json=commit_body,
                                 auth=self.database_auth).json()

        return len(response['results'][0]['data']) == 1

    def save_node(self, node: NodeIn):
        """
        Send request to database by its API to create new node

        Args:
            node (NodeIn): Node to be added to database

        Returns:
            Result of request as node object
        """
        create_template = string.Template("CREATE (n:$labels) RETURN n")
        create_statement = create_template.substitute(
            labels=":".join(list(node.labels))
        )

        commit_body = {
            "statements": [{"statement": create_statement}]
        }

        response = requests.post(url=self.database_url,
                                 json=commit_body,
                                 auth=self.database_auth).json()
        if len(response["errors"]) > 0:
            result = NodeOut(errors=response["errors"])
        else:
            node_id = response["results"][0]["data"][0]["meta"][0]["id"]
            result = NodeOut(id=node_id, labels=node.labels)

        return result

    def save_properties(self, id: int, properties: List[PropertyIn]):
        """
        Send request to database by its API to create new properties

        Args:
            id (int): Id of the node

            properties (List[PropertyIn]): List of properties for the node of given id

        Returns:
            Result of request as node object
        """
        if self.node_exists(id):
            create_statement = f"MATCH (n) where id(n)={id} SET n = $props return n"
            commit_body = {
                "statements": [{"statement": create_statement,
                                "parameters": {
                                    "props": {
                                        property.key: property.value for property in properties
                                    }
                                }}]
            }
            response = requests.post(url=self.database_url,
                                     json=commit_body,
                                     auth=self.database_auth).json()
            if len(response["errors"]) > 0:
                result = NodeOut(errors=response["errors"])
            else:
                node_id = response["results"][0]["data"][0]["meta"][0]["id"]
                result = NodeOut(id=node_id, properties=properties)
        else:
            result = NodeOut(id=id, errors={"errors": "not matching id"})

        return result
