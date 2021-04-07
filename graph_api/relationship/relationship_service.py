import requests
from database_service import DatabaseService
from database_config import database
from relationship.relationship_model import RelationshipOut, RelationshipIn


class RelationshipService:
    """
    Object to handle logic of relationships requests

    Attributes:
        db (DatabaseService): Handles communication with Neo4j database
    """
    db = DatabaseService()

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
