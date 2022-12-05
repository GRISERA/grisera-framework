import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from models.not_found_model import *
from registered_channel.registered_channel_model import *
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB


class TestRegisteredChannelServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_delete_registered_channel_without_error(self, get_node_relationships_mock, get_node_mock,
                                                     delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
                                                                      'properties': [{'key': 'age', 'value': 5}],
                                                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        registered_channel = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
                                                  relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                                 relation_id=0)],
                                                  reversed_relations=[RelationInformation(second_node_id=15,
                                                                                          name="testReversedRelation",
                                                                                          relation_id=0)])
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.delete_registered_channel(id_node)

        self.assertEqual(result, registered_channel)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_registered_channel_without_participant_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.delete_registered_channel(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_registered_channel_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.delete_registered_channel(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
