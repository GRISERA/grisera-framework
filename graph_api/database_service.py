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

    def create_properties(self, id, properties, object_part, return_part):
        """
        Send to the database request to add properties

        Args:
            id (int): Id of node or relationship
            properties (List[PropertyIn]): Properties to add
            object_part (str): Part of statement used to identify object type
            return_part (str): Part of statement used to return proper information
        Returns:
            Result of request      
        """
        set_part = ''.join(map(lambda property: 'x.{}="{}", '.format(property.key, property.value), properties))
        create_statement = "MATCH {} where id(x)={} SET {} return {}, x".format(
            object_part, id, set_part[:-2], return_part)
        commit_body = {
            "statements": [{"statement": create_statement}]
        }
        return self.post(commit_body)

    def create_relationship_properties(self, id, properties):
        """
        Create properties in database for relationship

        Args:
            id (int): Id of node or relationship
            properties (List[PropertyIn]): Properties to add

        Returns:
            Result of request
        """
        relation_part = "(n)-[x]->(m)"
        return_part = "id(n), type(x), id(m)"
        return self.create_properties(id, properties, relation_part, return_part)

    def create_node_properties(self, id, properties):
        """
        Create properties in database for node

        Args:
            id (int): Id of node or relationship
            properties (List[PropertyIn]): Properties to add

        Returns:
            Result of request
        """
        node_part = "(x)"
        return_part = "labels(x)"
        return self.create_properties(id, properties, node_part, return_part)
