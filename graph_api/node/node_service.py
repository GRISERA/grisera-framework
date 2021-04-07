import requests
import string
from functools import reduce
from requests.auth import HTTPBasicAuth
from database_config import database
from node.node_model import NodeIn, NodeOut


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
