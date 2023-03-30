import requests
from requests.auth import HTTPBasicAuth

from database_config import database
from node.node_model import NodeRowsQueryIn


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

    def post_statement(self, statement, database_name):
        """
        Wrap statement with body and send it to database by its API

        Args:
            statement (string): Statement to be sent
            database_name (string): Name of the database

        Returns:
            Result of request      
        """

        # self.database_url = replace_db_name(self.database_url, database_name)
        commit_body = {
            "statements": [{"statement": statement}]
        }
        response = self.post(commit_body, database_name)
        return response

    def post(self, commit_body, database_name):
        """
        Send request to database by its API

        Args:
            statement (string): Statement to be sent
            database_name (string): Name of the database

        Returns:
            Result of request      
        """
        print("###### COMMIT BODY: ", commit_body)

        self.database_url = self.replace_db_name(self.database_url, database_name)

        response = requests.post(url=self.database_url,
                                 json=commit_body,
                                 auth=self.database_auth).json()

        print("||||| GRAPH API: RESPONSE: ", response)

        return response

    def create_database_with_name(self, database_to_create):
        create_statement = "create database " + database_to_create

        # It don't have to be 'neo4j', any existing database is needed
        database_name = "neo4j"

        return self.post_statement(create_statement, database_name)

    def show_databases_with_name(self, database_name):
        statement = "show databases"
        return self.post_statement(statement, database_name)

    def check_if_database_exists(self, database_name):
        check_node_statement = "SHOW databases"
        response = self.post_statement(check_node_statement, database_name)
        for db in response['results'][0]['data']:
            db_name = db['row'][0]
            if database_name is db_name:
                return True
        return False

    def node_exists(self, node_id, database_name):
        """
        Check whether node with given id exists

        Args:
            node_id (int): node id to be checked
            database_name (string): Name of the database

        Returns:
            True if exists, otherwise false 
        """

        check_node_statement = "MATCH (n) where id(n) ={node_id} return n".format(node_id=node_id)
        response = self.post_statement(check_node_statement, database_name)
        return len(response['results']) != 0 and len(response['results'][0]['data']) == 1

    def create_node(self, node, database_name):
        """
        Send to the database request to create node

        Args:
            node (): node to be created
            database_name (string): Name of the database

        Returns:
            Result of request      
        """

        create_statement = "CREATE (n:{labels}) RETURN n".format(
                  labels=":".join(list(node.labels)))

        return self.post_statement(create_statement, database_name)

    def get_node(self, node_id, database_name):
        """
        Send to the database request to get node with given id

        Args:
            node_id (): id to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        get_statement = f"MATCH (n) WHERE id(n)={node_id} RETURN n, labels(n)"
        return self.post_statement(get_statement, database_name)

    def get_nodes(self, label, database_name):
        """
        Send to the database request to get nodes with given label

        Args:
            label (): label to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        get_statement = "MATCH (n: {label}) RETURN n".format(
            label=label)
        return self.post_statement(get_statement, database_name)

    def get_nodes_by_query(self, query: NodeRowsQueryIn, database_name):
        """
        Send to the database request to get nodes with given query
        Args:
            query (NodeRowsQueryIn): query to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        operators = {
            "equals": "=",
            "less": "<=",
            "greater": ">="
        }
        return_list = []
        where_list = []
        match_list = []
        if query.relations is not None:
            for relation in query.relations:
                statement = f"(n_{str(relation.begin_node_index)})-["
                if relation.label is not None:
                    statement += f":`{relation.label}`"
                if relation.min_count is not None:
                    statement += f"*{str(relation.min_count)}.."
                statement += f"]->(n_{str(relation.end_node_index)})"
                match_list.append(statement)

        element_id = 0
        for node in query.nodes:
            node_label = f"n_{str(element_id)}"
            statement = f"({node_label}"
            if node.result:
                return_list.append(node_label)
            if node.id is not None:
                where_list.append(f"ID({node_label})={str(node.id)}")
            if node.parameters is not None:
                for parameter in node.parameters:
                    if parameter.operator in operators:
                        operator = operators[parameter.operator]
                        if operator == "=":
                            where_list.append(f"{node_label}.{parameter.key}{operator}'{parameter.value}'")
                        else:
                            where_list.append(f"toInteger({node_label}.{parameter.key}){operator}{parameter.value}")
            if node.label is not None:
                statement += f":`{node.label}`"
            statement += ")"
            match_list.append(statement)
            element_id += 1
        get_statement = f"MATCH {','.join(match_list)}"
        if len(where_list) > 0:
            get_statement += f" WHERE {' AND '.join(where_list)}"
        if len(return_list) > 0:
            get_statement += f" RETURN {','.join([f'{label},LABELS({label})' for label in return_list])}"
        return self.post_statement(get_statement, database_name)

    def delete_node(self, node_id, database_name):
        """
        Send to the database request to delete node with given id

        Args:
            node_id (): Id to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        delete_statement = f"MATCH (n) WHERE id(n)={node_id} DETACH DELETE n return n"
        return self.post_statement(delete_statement, database_name)

    def relationship_exist(self, relationship_id, database_name):
        """
        Check if relationship exists in the database
        Args:
            relationship_id(int): id of the relationship
            database_name (string): Name of the database

        Returns:
            True - If there is a relationship in the database.
            False - If there is not a relationship in the database.
        """
        check_relationship_statement = "MATCH ()-[r]->() where id(r) ={relationship_id} return r".format(
            relationship_id=relationship_id)

        response = self.post_statement(check_relationship_statement, database_name)
        return len(response['results']) != 0 and len(response['results'][0]['data']) == 1

    def get_relationship(self, relationship_id, database_name):
        """
        Send to the database request to get relationship

        Args:
            relationship_id (): Relationship to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        get_statement = "MATCH ()-[r]->() where id(r)={} " \
                        "return id(startNode(r)), id(endNode(r)), type(r), id(r)".format(relationship_id)
        return self.post_statement(get_statement, database_name)

    def delete_relationship(self, relationship_id, database_name):
        """
        Send to the database request to delete relationship with given id

        Args:
            relationship_id (): Id to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        delete_statement = f"MATCH ()-[r]->() WHERE id(r)={relationship_id} DETACH DELETE r return r"
        return self.post_statement(delete_statement, database_name)

    def get_relationships(self, node_id, database_name):
        """
        Send to the database request to get relationships of node

        Args:
            node_id (): node to search by
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        get_statement = "MATCH (n)-[r]->(m) where id(n)={} or id(m)={} " \
                        "return id(startNode(r)), id(endNode(r)), type(r), id(r)".format(
            node_id, node_id)
        return self.post_statement(get_statement, database_name)

    def create_relationship(self, relationship, database_name):
        """
        Send to the database request to create relationship

        Args:
            relationship (): relationship to be created
            database_name (string): Name of the database

        Returns:
            Result of request      
        """
        create_statement = ("MATCH (n) where id(n) ={start_node} MATCH (m) where " +
                            "id(m) = {end_node} MERGE (n) - [r:{name}] -> (m) " +
                            "RETURN r").format(start_node=relationship.start_node,
                                               end_node=relationship.end_node,
                                               name=relationship.name)
        return self.post_statement(create_statement, database_name)

    def create_properties(self, id, properties, object_part, return_part, database_name):
        """
        Send to the database request to add properties

        Args:
            id (int): Id of node or relationship
            properties (List[PropertyIn]): Properties to add
            object_part (str): Part of statement used to identify object type
            return_part (str): Part of statement used to return proper
            database_name (string): Name of the database

        Returns:
            Result of request      
        """
        set_part = ''.join(map(lambda property: 'x.{}="{}", '.format(property.key, property.value), properties))
        create_statement = "MATCH {} where id(x)={} SET {} return {}, x".format(
            object_part, id, set_part[:-2], return_part)
        commit_body = {
            "statements": [{"statement": create_statement}]
        }
        return self.post(commit_body, database_name)

    def create_relationship_properties(self, id, properties, database_name):
        """
        Create properties in database for relationship

        Args:
            id (int): Id of node or relationship
            properties (List[PropertyIn]): Properties to add
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        relation_part = "(n)-[x]->(m)"
        return_part = "id(n), type(x), id(m)"
        return self.create_properties(id, properties, relation_part, return_part, database_name)

    def create_node_properties(self, id, properties, database_name):
        """
        Create properties in database for node

        Args:
            id (int): Id of node or relationship
            properties (List[PropertyIn]): Properties to add
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        node_part = "(x)"
        return_part = "labels(x)"
        return self.create_properties(id, properties, node_part, return_part, database_name)

    def delete_node_properties(self, id, database_name):
        """
        Send to the database request to delete properties from node

        Args:
            id (int): Id of node
            database_name (string): Name of the database

        Returns:
            Result of request
        """
        delete_statement = "MATCH (x) where id(x)=" + str(id) + " SET x ={} return x"
        commit_body = {
            "statements": [{"statement": delete_statement}]
        }
        return self.post(commit_body, database_name)

    def replace_string_between_two_substring(self, original_string, delimiter_before, delimiter_after,
                                             replacement_string):
        """
        Replace the substring in the original string with the replacement string.
        The substring to replace is between two substrings (delimiters) given as parameters.

        Args:
            original_string (str): original string
            delimiter_before (str): delimiter before the substring to replace
            delimiter_after (str): delimiter after the substring to replace
            replacement_string (str): string to replace in the place of substring between two delimiters
        Returns:
            String with replaced substring.
        """
        leading_text = original_string.split(delimiter_before)[0]
        trailing_text = original_string.split(delimiter_after)[1]
        return leading_text + delimiter_before + replacement_string + delimiter_after + trailing_text

    def replace_db_name(self, current_url, database_name):
        """
        Replace the name of currently used database by modifying the url used for sending requests to database.

        Args:
            current_url (str): current url used for request to the database
            database_name (str): the database name to switch into
        Returns:
            The url with new database name.
        """
        # url = "http://host.docker.internal:7474/db/dba/tx/commit"
        # new_database_name = 'DATABASE_NAME'
        new_url = self.replace_string_between_two_substring(current_url, '/db/', '/tx', database_name)
        # new_url = "http://host.docker.internal:7474/db/DATABASE_NAME/tx/commit"
        return new_url
