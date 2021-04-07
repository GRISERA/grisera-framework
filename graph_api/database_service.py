import requests
from requests.auth import HTTPBasicAuth
from database_config import database


class DatabaseService:
    """
    Object that handles communication with Neo4j database

    Attributes:
        database_url (str): Database URL 
        database_auth (HTTPBasicAuth): Database connection credentials
        _instance (DatabaseService): Instance of the singleton object
    """
    database_url = (database["address"] + database["commit_path"]) \
        .replace("{database_name}", database["name"])
    database_auth = HTTPBasicAuth(database["user"], database["passwd"])

    _instance = None

    def __new__(cls):
        """
        Creates singleton
        """
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def post_statement(self, statement):
        """
        Wrap statement with body and send it to database by its API

        Args:
            statement (string): Statement to be sent

        Returns:
            Result of request      
        """
        commit_body = {
            "statements": [{"statement": statement}]
        }
        response = self.post(commit_body)
        return response

    def post(self, commit_body):
        """
        Send request to database by its API

        Args:
            statement (string): Statement to be sent

        Returns:
            Result of request      
        """

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

        check_node_statement = "MATCH (n) where id(n) ={node_id} return n".format(
            node_id=node_id)
        response = self.post_statement(check_node_statement)
        return len(response['results']) != 0 and len(response['results'][0]['data']) == 1

    def create_node(self, node):
        """
        Send to the database request to create node

        Args:
            node (): node to be created

        Returns:
            Result of request      
        """
        create_statement = "CREATE (n:{labels}) RETURN n".format(
            labels=":".join(list(node.labels)))
        return self.post_statement(create_statement)

    def relationship_exist(self, relationship_id):
        """
        Check if relationship exists in the database
        Args:
            relationship_id(int): id of the relationship
        Returns:
            True - If there is a relationship in the database.
            False - If there is not a relationship in the database.
        """
        check_relationship_statement = "MATCH ()-[r]->() where id(r) ={relationship_id} return r".format(
            relationship_id=relationship_id)

        response = self.post_statement(check_relationship_statement)
        return len(response['results']) != 0 and len(response['results'][0]['data']) == 1

    def create_relationship(self, relationship):
        """
        Send to the database request to create relationship

        Args:
            relationship (): relationship to be created

        Returns:
            Result of request      
        """
        create_statement = ("MATCH (n) where id(n) ={start_node} MATCH (m) where " +
                            "id(m) = {end_node} MERGE (n) - [r:{name}] -> (m) " +
                            "RETURN r").format(start_node=relationship.start_node,
                                               end_node=relationship.end_node,
                                               name=relationship.name)
        return self.post_statement(create_statement)

    def create_properties(self, node_id: int, properties):
        """
        Send to the database request to create relationship

        Args:
            relationship (): relationship to be created

        Returns:
            Result of request      
        """
        create_statement = "MATCH (n) where id(n)={} SET n = $props return n".format(
            node_id)
        commit_body = {
            "statements": [{"statement": create_statement,
                            "parameters": {
                                "props": {
                                    property.key: property.value for property in properties
                                }
                            }}]
        }
        return self.post(commit_body)
