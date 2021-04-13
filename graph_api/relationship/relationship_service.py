from database_service import DatabaseService
from database_config import database
from relationship.relationship_model import RelationshipOut, RelationshipIn
from property.property_model import PropertyIn
from typing import List


class RelationshipService:
    """
    Object to handle logic of relationships requests

    Attributes:
        db (DatabaseService): Handles communication with Neo4j database
    """
    db: DatabaseService = DatabaseService()

    def save_relationship(self, relationship: RelationshipIn):
        """
        Send request to database by its API to create new relationship

        Args:
            relationship (-): Relationship to be added to database

        Returns:
            Result of request as relationship object
        """
        if self.db.node_exists(relationship.start_node) and self.db.node_exists(relationship.end_node):
            response = self.db.create_relationship(relationship)

            if len(response["errors"]) > 0:
                result = RelationshipOut(start_node=relationship.start_node, end_node=relationship.end_node,
                                         name=relationship.name, errors=response["errors"])
            else:
                relationship_id = response["results"][0]["data"][0]["meta"][0]["id"]
                result = RelationshipOut(start_node=relationship.start_node, end_node=relationship.end_node,
                                         name=relationship.name, id=relationship_id)
        else:
            result = RelationshipOut(start_node=relationship.start_node, end_node=relationship.end_node,
                                     name=relationship.name, errors={"errors": "not matching node id"})

        return result

    def save_properties(self, id: int, properties: List[PropertyIn]):
        """
        Send request to database by its API to create new properties

        Args:
            id (int): Id of the relationship

            properties (List[PropertyIn]): List of properties for the relationship of given id

        Returns:
            Result of request as relationship object
        """
        if self.db.relationship_exist(id):
            response = self.db.create_relationship_properties(id, properties)
            if len(response["errors"]) > 0:
                result = RelationshipOut(errors=response["errors"])
            else:
                response_data = response["results"][0]["data"][0]["row"]
                response_properties = list((map(
                    lambda property: PropertyIn(key=property[0], value=property[1]), response_data[3].items())))
                result = RelationshipOut(start_node=response_data[0], end_node=response_data[2], name=response_data[1],
                                         id=id, properties=response_properties)
        else:
            result = RelationshipOut(id=id, errors={"errors": "not matching id"})

        return result
