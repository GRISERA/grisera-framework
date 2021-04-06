import requests
from requests.auth import HTTPBasicAuth
from database_config import database
from relationship.relationshi_service import RelationshipOut

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

    def save_relationship(self, relationship):
        """
        Send request to database by its API to create new relationship

        Args:
            relationship (-): Relationship to be added to database

        Returns:

        """
        # if start_node and end_node nie istnieje ?

        create_statement = "MATCH(n {" + f"{relati}" + "}), (m { " + f"{end_node}" + "}) CREATE (n)-[:" + f"{relationship}" + "]->(m)"
        commit_body = {
            "statements": [{"statement": create_statement}]
        }
        result = requests.post(url=self.database_url,
                               json=commit_body,
                               auth=self.database_auth).json()
        if len(result["errors"]) > 0:
             result = RelationshipOut(errors=result["errors"])
        else:
            relationship_id = result["results"][0]["data"][0]["meta"][0]["id"]
            result = RelationshipOut(id=relationship_id)

        return result

