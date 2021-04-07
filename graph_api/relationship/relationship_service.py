import requests
from requests.auth import HTTPBasicAuth
from database_config import database
from relationship.relationship_model import RelationshipOut, RelationshipIn


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
