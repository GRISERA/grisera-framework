import requests
from requests.auth import HTTPBasicAuth
from database_config import database
from relationship.relationship_model import RelationshipOut, RelationshipIn
from property.property_model import PropertyIn
from typing import List


class RelationshipService:
    """
    Object to handle logic of relationships requests

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

    def relationship_exist(self, relationship_id):
        """
        Check if relationship exists in the database

        Args:
            relationship_id(int): id of the relationship

        Returns:
            True - If there is a relationship in the database.
            False - If there is not a relationship in the database.
        """
        check_relationship_statement = f"MATCH ()-[r]->() where id(r) ={relationship_id} return r"
        commit_body = {
            "statements": [{"statement": check_relationship_statement}]
        }
        response = requests.post(url=self.database_url,
                                 json=commit_body,
                                 auth=self.database_auth).json()

        return len(response['results'][0]['data']) == 1

    def save_relationship(self, relationship: RelationshipIn):
        """
        Send request to database by its API to create new relationship

        Args:
            relationship (-): Relationship to be added to database

        Returns:
            Result of request as relationship object
        """
        if self.node_exists(relationship.start_node) and self.node_exists(relationship.end_node):
            create_statement = f"MATCH (n) where id(n) ={relationship.start_node} MATCH (m) where id(m) = {relationship.end_node} MERGE (n) - [r:{relationship.name}] -> (m) RETURN r"
            commit_body = {
                "statements": [{"statement": create_statement}]
            }
            response = requests.post(url=self.database_url,
                                     json=commit_body,
                                     auth=self.database_auth).json()

            if len(response["errors"]) > 0:
                result = RelationshipOut(start_node=relationship.start_node, end_node=relationship.end_node,
                                         name=relationship.name, errors=response["errors"])
            else:
                relationship_id = response["results"][0]["data"][0]["meta"][0]["id"]
                result = RelationshipOut(start_node=relationship.start_node, end_node=relationship.end_node,
                                         name=relationship.name, id=relationship_id)
        else:
            result = RelationshipOut(start_node=relationship.start_node, end_node=relationship.end_node,
                                     name=relationship.name, errors={"errors": "not matching id"})

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
        if self.relationship_exist(id):
            create_statement = f"MATCH ()-[r]->() where id(r)={id} set r = $props return r"
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
                result = RelationshipOut(errors=response["errors"])
            else:
                relationship_id = response["results"][0]["data"][0]["meta"][0]["id"]
                result = RelationshipOut(id=relationship_id, properties=properties)
        else:
            result = RelationshipOut(id=id, errors={"errors": "not matching id"})

        return result
    

