import json
import unittest
import unittest.mock as mock

from requests import Response

from activity_execution.activity_execution_model import ActivityExecutionIn
from graph_api_service import GraphApiService
from time_series.time_series_model import TimeSeriesTransformationRelationshipIn


class DatabaseServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.graph_api_service = GraphApiService()
        self.response_content = {'id': 1, 'errors': [], 'links': {}}
        self.response = Response()
        self.response._content = json.dumps(self.response_content).encode('utf-8')

    @mock.patch('graph_api_service.requests')
    def test_post(self, requests_mock):
        dataset_name = "neo4j"
        requests_mock.post.return_value = self.response
        url_part = '/nodes'
        node = {}

        result = self.graph_api_service.post(url_part, node, dataset_name)
        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.graph_api_service.graph_api_url + url_part + "?dataset_name=" + dataset_name,
                           json=node)

    @mock.patch('graph_api_service.requests')
    def test_get(self, requests_mock):
        dataset_name = "neo4j"
        requests_mock.get.return_value = self.response
        url_part = '/nodes'
        params = {'label': 'Test'}

        result = self.graph_api_service.get(url_part, params, dataset_name)

        self.assertEqual(result, self.response_content)
        requests_mock.get.assert_called_with(url=self.graph_api_service.graph_api_url + url_part + "?dataset_name=" + dataset_name,
                                                params=params)

    @mock.patch('graph_api_service.requests')
    def test_delete(self, requests_mock):
        dataset_name = "neo4j"
        requests_mock.delete.return_value = self.response
        url_part = '/nodes'
        params = {'label': 'Test'}

        result = self.graph_api_service.delete(url_part, params, dataset_name)

        self.assertEqual(result, self.response_content)
        requests_mock.delete.assert_called_with(url=self.graph_api_service.graph_api_url + url_part + "?dataset_name=" + dataset_name,
                                                params=params)

    @mock.patch.object(GraphApiService, 'post')
    def test_create_node(self, post_mock):
        dataset_name = "neo4j"
        post_mock.return_value = self.response_content
        label = 'Test'

        result = self.graph_api_service.create_node(label, dataset_name)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with('/nodes', {"labels": [label], "dataset_name": [dataset_name]}, dataset_name)

    @mock.patch.object(GraphApiService, 'get')
    def test_get_nodes(self, get_mock):
        dataset_name = "neo4j"
        get_mock.return_value = self.response_content
        label = 'Test'

        result = self.graph_api_service.get_nodes(label, dataset_name)

        self.assertEqual(result, self.response_content)
        get_mock.assert_called_with('/nodes', {"label": label, "dataset_name": dataset_name}, dataset_name)

    @mock.patch.object(GraphApiService, 'get')
    def test_get_node_relationships(self, get_mock):
        dataset_name = "neo4j"
        get_mock.return_value = self.response_content
        node_id = 1

        result = self.graph_api_service.get_node_relationships(node_id, dataset_name)

        self.assertEqual(result, self.response_content)
        get_mock.assert_called_with('/nodes/1/relationships', {"dataset_name": dataset_name}, dataset_name)

    @mock.patch.object(GraphApiService, 'delete')
    def test_delete_node(self, delete_mock):
        dataset_name = "neo4j"
        delete_mock.return_value = self.response_content
        node_id = 1

        result = self.graph_api_service.delete_node(node_id, dataset_name)

        self.assertEqual(result, self.response_content)
        delete_mock.assert_called_with('/nodes/1', {"dataset_name": dataset_name}, dataset_name)

    @mock.patch.object(GraphApiService, 'post')
    def test_create_properties(self, post_mock):
        dataset_name = "neo4j"
        post_mock.return_value = self.response_content
        node_id = 1
        node_model = ActivityExecutionIn(activity_id=1, arrangement_id=2,
                                         identifier=1, additional_properties=[{'key': 'test', 'value': 'test'}])

        result = self.graph_api_service.create_properties(node_id, node_model, dataset_name)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with("/nodes/1/properties",
                                     [{'key': 'activity_id', 'value': 1, "dataset_name": dataset_name},
                                      {'key': 'arrangement_id', 'value': 2, "dataset_name": dataset_name},
                                      {'key': 'test', 'value': 'test'}], dataset_name)

    @mock.patch.object(GraphApiService, 'post')
    def test_create_relationships(self, post_mock):
        dataset_name = "neo4j"
        post_mock.return_value = self.response_content
        start_node = 1
        end_node = 2
        name = 'hasNode'

        result = self.graph_api_service.create_relationships(start_node, end_node, name, dataset_name)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with("/relationships", {"start_node": 1, "end_node": 2, "name": 'hasNode',
                                                        "dataset_name": [dataset_name]}, dataset_name)

    @mock.patch.object(GraphApiService, 'delete')
    def test_delete_relationship(self, delete_mock):
        dataset_name = "neo4j"
        delete_mock.return_value = self.response_content
        relationship_id = 1

        result = self.graph_api_service.delete_relationship(relationship_id, dataset_name)

        self.assertEqual(result, self.response_content)
        delete_mock.assert_called_with('/relationships/1', {"dataset_name": dataset_name}, dataset_name)

    def test_create_additional_properties(self):
        property_dict = {'additional_properties': [{'key': 'test', 'value': 'test'},
                                                   {'key': 'key', 'value': 'value'}]}

        result = self.graph_api_service.create_additional_properties(property_dict)

        self.assertEqual(result, [{'key': 'test', 'value': 'test'}, {'key': 'key', 'value': 'value'}])

    @mock.patch.object(GraphApiService, 'post')
    def test_create_relationship_properties(self, post_mock):
        dataset_name = "neo4j"
        post_mock.return_value = self.response_content
        relationship_id = 1
        relationship_model = TimeSeriesTransformationRelationshipIn(
            additional_properties=[{'key': 'test', 'value': '1234'}])

        result = self.graph_api_service.create_relationship_properties(relationship_id, relationship_model, dataset_name)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with("/relationships/1/properties", [{'key': 'test', 'value': '1234'}], dataset_name)
