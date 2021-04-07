import string
import requests
from requests.auth import HTTPBasicAuth
from database_config import database


class DatabaseService:
    """
    Object that handles communication with Neo4j database

    Attributes:
        database_url (str): Database URL 
        database_auth (HTTPBasicAuth): Database connection credentials
        check_node_template (string.Template): Template for checking the node
        create_node_template (string.Template): Template for creating the node
        create_relationship_template (string.Template): Template for creating the relationship
        _instance (DatabaseService): Instance of the singleton object
    """
    database_url = (database["address"] + database["commit_path"]) \
        .replace("{database_name}", database["name"])
    database_auth = HTTPBasicAuth(database["user"], database["passwd"])

    check_node_template = string.Template(
        "MATCH (n) where id(n) =$node_id return n")
    create_node_template = string.Template("CREATE (n:$labels) RETURN n")
    create_relationship_template = string.Template("MATCH (n) where id(n) =$start_node MATCH (m) where id(m) = "
                                                   "$end_node MERGE (n) - [r:$name] -> (m) RETURN r")

    _instance = None

    def __new__(cls):
        """
        Creates singleton
        """
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def post(self, statement):
        """
        Send request to database by its API

        Args:
            statement (string): Statement to be sent

        Returns:
            Result of request      
        """
        commit_body = {
            "statements": [{"statement": statement}]
        }
        response = requests.post(url=self.database_url,
                                 json=commit_body,
                                 auth=self.database_auth).json()
        return response

    def node_exists(self, node_id):
        """
        Check wheather node with given id exists

        Args:
            node_id (int): node id to be checked

        Returns:
            True if exists, otherwise false 
        """
        check_node_statement = self.check_node_template.substitute(
            node_id=node_id)
        response = self.post(check_node_statement)
        return len(response['results']) != 0 and len(response['results'][0]['data']) == 1

    def create_node(self, node):
        """
        Send to the database request to create node

        Args:
            node (): node to be created

        Returns:
            Result of request      
        """
        create_statement = self.create_node_template.substitute(
            labels=":".join(list(node.labels))
        )
        return self.post(create_statement)

    def create_relationship(self, relationship):
        """
        Send to the database request to create relationship

        Args:
            relationship (): relationship to be created

        Returns:
            Result of request      
        """
        create_statement = self.create_relationship_template.substitute(start_node=relationship.start_node,
                                                                        end_node=relationship.end_node,
                                                                        name=relationship.name)
        return self.post(create_statement)
