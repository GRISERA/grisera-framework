import json
import unittest
import unittest.mock as mock

from requests import Response

from database_service import DatabaseService
from node.node_model import NodeIn, NodeRowsQueryIn, NodeQueryIn, RelationQueryIn
from property.property_model import PropertyIn
from relationship.relationship_model import RelationshipIn


class DatabaseServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.database_service = DatabaseService()
        self.statement = "Create (n: Test)"
        self.commit_body = {"statements": [{"statement": self.statement}]}
        self.response_content = {'results': [{'data': [{'meta': [{}]}]}], 'errors': []}
        self.response = Response()
        self.response._content = json.dumps(self.response_content).encode('utf-8')

    @mock.patch('database_service.requests')
    def test_post(self, requests_mock):
        requests_mock.post.return_value = self.response

        result = self.database_service.post(self.commit_body)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=self.commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_post_statement(self, requests_mock):
        requests_mock.post.return_value = self.response

        result = self.database_service.post_statement(self.statement)

        self.assertEqual(result, self.response_content)

    @mock.patch('database_service.requests')
    def test_node_exists_with_node(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH (n) where id(n) =1 return n"}]}
        node_id = 1

        result = self.database_service.node_exists(node_id)

        self.assertTrue(result)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json = commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_node_exists_without_node(self, requests_mock):
        response_content = {"results": [{"data": []}], "errors": []}
        response = Response()
        response._content = json.dumps(response_content).encode("utf-8")
        requests_mock.post.return_value = response
        node_id = 2

        result = self.database_service.node_exists(node_id)

        self.assertFalse(result)

    @mock.patch('database_service.requests')
    def test_create_node_with_one_label(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "CREATE (n:Test) RETURN n"}]}
        node = NodeIn(labels=["Test"])

        result = self.database_service.create_node(node)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_create_node_without_labels(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "CREATE (n:) RETURN n"}]}
        node = NodeIn()

        result = self.database_service.create_node(node)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_get_node(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH (n) WHERE id(n)=5 RETURN n, labels(n)"}]}
        node_id = 5

        result = self.database_service.get_node(node_id)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_get_nodes(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH (n: Test) RETURN n"}]}
        label = "Test"

        result = self.database_service.get_nodes(label)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_get_nodes_by_query(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{
            "statement": "MATCH (n_0)-[:`hasSignal`]->(n_1),(n_1)-[:`next`*0..]->(n_2),(n_3)-[:`startInSec`]->(n_2),(n_4)-[:`endInSec`]->(n_2),(n_0:`Time Series`),(n_1:`Signal Value`),(n_2:`Signal Value`),(n_3:`Timestamp`),(n_4:`Timestamp`) WHERE ID(n_0)=15 RETURN n_2,LABELS(n_2),n_3,LABELS(n_3),n_4,LABELS(n_4)"}]}
        query = NodeRowsQueryIn(
            nodes=[
                NodeQueryIn(id=15, label="Time Series"),
                NodeQueryIn(label="Signal Value"),
                NodeQueryIn(label="Signal Value", result=True),
                NodeQueryIn(label="Timestamp", result=True),
                NodeQueryIn(label="Timestamp", result=True),
            ],
            relations=[
                RelationQueryIn(begin_node_index=0, end_node_index=1, label="hasSignal"),
                RelationQueryIn(begin_node_index=1, end_node_index=2, label="next", min_count=0),
                RelationQueryIn(begin_node_index=3, end_node_index=2, label="startInSec"),
                RelationQueryIn(begin_node_index=4, end_node_index=2, label="endInSec"),
            ])

        result = self.database_service.get_nodes_by_query(query)

        self.assertEqual(self.response_content, result)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_delete_node(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH (n) WHERE id(n)=5 DETACH DELETE n return n"}]}
        node_id = 5

        result = self.database_service.delete_node(node_id)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_relationship_exist_with_relationship(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH ()-[r]->() where id(r) =1 return r"}]}
        relation_id = 1

        result = self.database_service.relationship_exist(relation_id)

        self.assertTrue(result)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_relationship_exist_without_relationship(self, requests_mock):
        response_content = {'results': [{'data': []}], 'errors': []}
        response = Response()
        response._content = json.dumps(response_content).encode('utf-8')
        requests_mock.post.return_value = response
        node_id = 2

        result = self.database_service.relationship_exist(node_id)

        self.assertFalse(result)

    @mock.patch('database_service.requests')
    def test_get_relationship(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH ()-[r]->() where id(r)=5 "
                                                    "return id(startNode(r)), id(endNode(r)), type(r), id(r)"}]}
        relationship_id = 5

        result = self.database_service.get_relationship(relationship_id)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_delete_relationship(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH ()-[r]->() WHERE id(r)=5 "
                                                    "DETACH DELETE r return r"}]}
        relationship_id = 5

        result = self.database_service.delete_relationship(relationship_id)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_get_relationships(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH (n)-[r]->(m) where id(n)=5 or id(m)=5 "
                                                    "return id(startNode(r)), id(endNode(r)), type(r), id(r)"}]}
        node_id = 5

        result = self.database_service.get_relationships(node_id)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_create_relationship(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": "MATCH (n) where id(n) =2 MATCH (m) where " +
                                                    "id(m) = 3 MERGE (n) - [r:Test] -> (m) " +
                                                    "RETURN r"}]}
        relation = RelationshipIn(start_node=2, end_node=3, name="Test")

        result = self.database_service.create_relationship(relation)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_create_properties(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": 'MATCH (x) where id(x)=2 SET x.key="value", ' +
                                                    'x.test="Test" return id(x), x'}]}
        properties = [PropertyIn(key="key", value="value"), PropertyIn(key="test", value="Test")]
        object_id = 2

        result = self.database_service.create_properties(object_id, properties, "(x)", "id(x)")

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_create_relationship_properties(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": 'MATCH (n)-[x]->(m) where id(x)=2 SET x.key="value", ' +
                                                    'x.test="Test" return id(n), type(x), id(m), x'}]}
        properties = [PropertyIn(key="key", value="value"), PropertyIn(key="test", value="Test")]
        object_id = 2

        result = self.database_service.create_relationship_properties(object_id, properties)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_create_node_properties(self, requests_mock):
        requests_mock.post.return_value = self.response
        commit_body = {"statements": [{"statement": 'MATCH (x) where id(x)=2 SET x.key="value", ' +
                                                    'x.test="Test" return labels(x), x'}]}
        properties = [PropertyIn(key="key", value="value"), PropertyIn(key="test", value="Test")]
        object_id = 2

        result = self.database_service.create_node_properties(object_id, properties)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)

    @mock.patch('database_service.requests')
    def test_delete_node_properties(self, requests_mock):
        requests_mock.post.return_value = self.response
        object_id = 2
        commit_body = {
            "statements": [{"statement": "MATCH (x) where id(x)="+str(object_id)+" SET x ={} return x"}]
        }
        result = self.database_service.delete_node_properties(object_id)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.database_service.database_url, json=commit_body,
                                              auth=self.database_service.database_auth)
