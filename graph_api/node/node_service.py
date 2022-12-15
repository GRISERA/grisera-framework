from typing import List

from database_service import DatabaseService
from node.node_model import NodeIn, NodeOut, BasicNodeOut, NodesOut, NodeRowsQueryIn, NodeRowsOut
from property.property_model import PropertyIn
from relationship.relationship_model import RelationshipsOut, BasicRelationshipOut


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

    def get_node(self, node_id: int):
        """
        Send request to database by its API to acquire node with given id

        Args:
            node_id (int): Id by which it is searched for in the database

        Returns:
            Acquired node in NodeOut model
        """
        response = self.db.get_node(node_id)

        if len(response['results'][0]["data"]) == 0:
            return NodeOut(errors="Node not found")

        node = response['results'][0]["data"][0]
        properties = [PropertyIn(key=property[0], value=property[1]) for property in node["row"][0].items()]
        result = NodeOut(id=node_id, properties=properties, labels={node["row"][1][0]})

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

    def get_nodes_by_query(self, query: NodeRowsQueryIn):
        """
        Send request to database by its API to acquire nodes with given query
        Args:
            query (NodeRowsQueryIn): Query by which it is searched for in the database
        Returns:
            List of acquired nodes in NodesOut model
        """
        response = self.db.get_nodes_by_query(query)

        if len(response["errors"]) > 0:
            return NodeRowsOut(errors=response["errors"])

        result = NodeRowsOut(rows=[])

        for nodes in response["results"][0]["data"]:
            row = []
            for i in range(len(nodes["row"]) // 2):
                properties = [PropertyIn(key=property[0], value=property[1]) for property in
                              nodes["row"][2 * i].items()]
                row.append(
                    BasicNodeOut(labels=nodes["row"][2 * i + 1], id=nodes["meta"][2 * i]["id"], properties=properties))
            result.rows.append(row)
        return result

    def delete_node(self, node_id: int):
        """
        Send request to database by its API to delete node with given id

        Args:
            node_id (int): Id of node
        Returns:
            Deleted node
        """
        node = self.get_node(node_id)
        response = self.db.delete_node(node_id)
        result = NodeOut(errors=response["errors"]) if len(response["errors"]) > 0 else \
            NodeOut(id=node_id, labels=node.labels, properties=node.properties)

        return result

    def get_relationships(self, id: int):
        """
        Send request to database by its API to get node's relationships

        Args:
            id (int): Id of the node

        Returns:
            Result of request as list of relationships
        """
        response = self.db.get_relationships(id)

        if len(response["errors"]) > 0:
            result = RelationshipsOut(errors=response["errors"])
        else:
            response_data = response["results"][0]["data"]
            relationships = [BasicRelationshipOut(start_node=relation["row"][0], end_node=relation["row"][1],
                                                  id=relation["row"][3], name=relation["row"][2]) for relation in response_data]
            result = RelationshipsOut(relationships=relationships)

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

    def delete_node_properties(self, node_id: int):
        """
        Send request to database by its API to delete properties from node with given id

        Args:
            node_id (int): Id of node
        Returns:
            Deleted node
        """
        node = self.get_node(node_id)
        response = self.db.delete_node_properties(node_id)
        result = NodeOut(errors=response["errors"]) if len(response["errors"]) > 0 else \
            NodeOut(id=node_id, labels=node.labels, properties=node.properties)

        return result
