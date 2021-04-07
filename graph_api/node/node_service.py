import requests
from database_service import DatabaseService
from node.node_model import NodeIn, NodeOut


class NodeService:
    """
    Object to handle logic of nodes requests

    Attributes:
        db (DatabaseService): Handles communication with Neo4j database
    """

    db = DatabaseService()

    def save_node(self, node: NodeIn):
        """
        Send request to database by its API to create new node

        Args:
            node (NodeIn): Node to be added to database

        Returns:
            Result of request as node object
        """
        response = self.db.create_node(node)

        if len(response["errors"]) > 0:
            result = NodeOut(errors=response["errors"])
        else:
            node_id = response["results"][0]["data"][0]["meta"][0]["id"]
            result = NodeOut(id=node_id, labels=node.labels)

        return result
