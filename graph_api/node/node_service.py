import requests
from requests.auth import HTTPBasicAuth
from ..database_config import database
from .node_model import NodeOut


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

    def save_node(self, node):
        """
        Send request to database by its API to create new node

        Args:
            node (NodeIn): Node to be added to database

        Returns:
            Result of request as node object
        """
        create_statement = "CREATE (n) RETURN n"
        for label in node.labels:
            create_statement = create_statement[:-10] + f":{label}" + create_statement[-10:]

        commit_body = {
            "statements": [{"statement": create_statement}]
        }

        result = requests.post(url=self.database_url,
                               json=commit_body,
                               auth=self.database_auth).json()
        if len(result["errors"]) > 0:
            result = NodeOut(errors=result["errors"])
        else:
            node_id = result["results"][0]["data"][0]["meta"][0]["id"]
            result = NodeOut(id=node_id, labels=node.labels)

        return result
