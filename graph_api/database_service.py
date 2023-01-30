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

    def get_node(self, node_id):
        """
        Send to the database request to get node with given id

        Args:
            node_id (): id to search by

        Returns:
            Result of request
        """
        get_statement = f"MATCH (n) WHERE id(n)={node_id} RETURN n, labels(n)"
        return self.post_statement(get_statement)

    def get_nodes(self, label):
        """
        Send to the database request to get nodes with given label

        Args:
            label (): label to search by

        Returns:
            Result of request
        """
        get_statement = "MATCH (n: {label}) RETURN n".format(
            label=label)
        return self.post_statement(get_statement)

    def get_nodes_by_query(self, query: NodeRowsQueryIn):
        """
        Send to the database request to get nodes with given query
        Args:
            query (NodeRowsQueryIn): query to search by
        Returns:
            Result of request
        """
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
                for parameter, value in node.parameters.items():
                    where_list.append(f"{node_label}.{parameter}='{value}'")
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
        return self.post_statement(get_statement)

    def delete_node(self, node_id):
        """
        Send to the database request to delete node with given id

        Args:
            node_id (): Id to search by

        Returns:
            Result of request
        """
        delete_statement = f"MATCH (n) WHERE id(n)={node_id} DETACH DELETE n return n"
        return self.post_statement(delete_statement)

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

    def get_relationship(self, relationship_id):
        """
        Send to the database request to get relationship

        Args:
            relationship_id (): Relationship to search by

        Returns:
            Result of request
        """
        get_statement = "MATCH ()-[r]->() where id(r)={} " \
                        "return id(startNode(r)), id(endNode(r)), type(r), id(r)".format(relationship_id)
        return self.post_statement(get_statement)

    def delete_relationship(self, relationship_id):
        """
        Send to the database request to delete relationship with given id

        Args:
            relationship_id (): Id to search by

        Returns:
            Result of request
        """
        delete_statement = f"MATCH ()-[r]->() WHERE id(r)={relationship_id} DETACH DELETE r return r"
        return self.post_statement(delete_statement)

    def get_relationships(self, node_id):
        """
        Send to the database request to get relationships of node

        Args:
            node_id (): node to search by

        Returns:
            Result of request
        """
        get_statement = "MATCH (n)-[r]->(m) where id(n)={} or id(m)={} " \
                        "return id(startNode(r)), id(endNode(r)), type(r), id(r)".format(
                         node_id, node_id)
        return self.post_statement(get_statement)

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

    def delete_node_properties(self, id):
        """
        Send to the database request to delete properties from node

        Args:
            id (int): Id of node
        Returns:
            Result of request
        """
        delete_statement = "MATCH (x) where id(x)="+str(id)+" SET x ={} return x"
        commit_body = {
            "statements": [{"statement": delete_statement}]
        }
        return self.post(commit_body)
