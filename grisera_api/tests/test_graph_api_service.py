import json
import unittest
import unittest.mock as mock

from activity.activity_model import ActivityIn
from graph_api_service import GraphApiService
from requests import Response


class DatabaseServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.graph_api_service = GraphApiService()
        self.response_content = {'id': 1, 'errors': [], 'links': {}}
        self.response = Response()
        self.response._content = json.dumps(self.response_content).encode('utf-8')

    @mock.patch('graph_api_service.requests')
    def test_post(self, requests_mock):
        requests_mock.post.return_value = self.response
        url_part = '/nodes'
        node = {}

        result = self.graph_api_service.post(url_part, node)

        self.assertEqual(result, self.response_content)
        requests_mock.post.assert_called_with(url=self.graph_api_service.graph_api_url + url_part,
                                              json=node)

    @mock.patch('graph_api_service.requests')
    def test_get(self, requests_mock):
        requests_mock.get.return_value = self.response
        url_part = '/nodes'
        params = {'label': 'Test'}

        result = self.graph_api_service.get(url_part, params)

        self.assertEqual(result, self.response_content)
        requests_mock.get.assert_called_with(url=self.graph_api_service.graph_api_url + url_part,
                                             params=params)

    @mock.patch.object(GraphApiService, 'post')
    def test_create_node(self, post_mock):
        post_mock.return_value = self.response_content
        label = 'Test'

        result = self.graph_api_service.create_node(label)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with('/nodes', {"labels": [label]})

    @mock.patch.object(GraphApiService, 'get')
    def test_get_nodes(self, get_mock):
        get_mock.return_value = self.response_content
        label = 'Test'

        result = self.graph_api_service.get_nodes(label)

        self.assertEqual(result, self.response_content)
        get_mock.assert_called_with('/nodes', {"label": label})

    @mock.patch.object(GraphApiService, 'post')
    def test_create_properties(self, post_mock):
        post_mock.return_value = self.response_content
        node_id = 1
        node_model = ActivityIn(identifier=1, additional_properties=[{'key': 'test', 'value': 'test'}])

        result = self.graph_api_service.create_properties(node_id, node_model)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with("/nodes/1/properties", [{'key': 'identifier', 'value': 1},
                                                             {'key': 'test', 'value': 'test'}])

    @mock.patch.object(GraphApiService, 'post')
    def test_create_relationships(self, post_mock):
        post_mock.return_value = self.response_content
        start_node = 1
        end_node = 2
        name = 'hasNode'

        result = self.graph_api_service.create_relationships(start_node, end_node, name)

        self.assertEqual(result, self.response_content)
        post_mock.assert_called_with("/relationships", {"start_node": 1, "end_node": 2, "name": 'hasNode'})

    def test_create_additional_properties(self):
        property_dict = {'additional_properties': [{'key': 'test', 'value': 'test'},
                                                   {'key': 'key', 'value': 'value'}]}

        result = self.graph_api_service.create_additional_properties(property_dict)

        self.assertEqual(result, [{'key': 'test', 'value': 'test'}, {'key': 'key', 'value': 'value'}])

