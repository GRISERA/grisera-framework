from database_service import DatabaseService
from node.node_model import NodeIn, NodeOut, BasicNodeOut, NodesOut
from property.property_model import PropertyIn
from typing import List


class NodeService:
    """
    Object to handle logic of nodes requests

    Attributes:
        db (DatabaseService): Handles communication with Neo4j database
    """

    db : DatabaseService = DatabaseService()

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

    def get_nodes(self, label: str):
        """
        Send request to database by its API to acquire all nodes with given label

        Args:
            label (str): Label by which it is searched for in the database

        Returns:
            List of acquired nodes in NodesOut model
        """
        response = self.db.get_nodes(label)

        if len(response["errors"]) > 0:
            return NodesOut(errors=response["errors"])

        result = NodesOut(nodes=[])
        for node in response["results"][0]["data"]:
            properties = [PropertyIn(key=property[0], value=property[1]) for property in node["row"][0].items()]
            result.nodes.append(BasicNodeOut(labels={label}, id=node["meta"][0]["id"], properties=properties))

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
        if self.db.node_exists(id):
            response = self.db.create_node_properties(id, properties)
            if len(response["errors"]) > 0:
                result = NodeOut(errors=response["errors"])
            else:
                response_data = response["results"][0]["data"][0]["row"]
                response_properties = list((map(
                    lambda property: PropertyIn(key=property[0], value=property[1]), response_data[1].items())))
                result = NodeOut(labels=set(response_data[0]), id=id, properties=response_properties)
        else:
            result = NodeOut(id=id, errors={"errors": "not matching id"})

        return result
