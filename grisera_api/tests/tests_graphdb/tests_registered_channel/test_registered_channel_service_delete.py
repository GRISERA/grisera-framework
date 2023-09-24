import unittest
import unittest.mock as mock

from channel.channel_model import BasicChannelOut
from graph_api_service import GraphApiService
from models.not_found_model import *
from recording.recording_model import BasicRecordingOut
from registered_channel.registered_channel_model import *
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from registered_data.registered_data_model import BasicRegisteredDataOut


class TestRegisteredChannelServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_registered_channel_without_error(self,get_node_mock,
                                                     delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Registered_Channel'],
                                                                      'properties': [{'key': 'age', 'value': 5}],
                                                                      "errors": None, 'links': None}
        registered_channel = BasicRegisteredChannelOut(age=5, id=id_node, additional_properties=[])
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.delete_registered_channel(id_node)

        self.assertEqual(result, registered_channel)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

        # @mock.patch.object(GraphApiService, 'delete_node')
        # @mock.patch.object(GraphApiService, 'get_node')
        # @mock.patch.object(GraphApiService, 'get_node_relationships')
        # def test_delete_registered_channel_without_error(self, get_node_relationships_mock, get_node_mock,
        #                                                  delete_node_mock):
        #     id_node = 1
        #     delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node,
        #                                                                   'labels': ['Registered_Channel'],
        #                                                                   'properties': [{'key': 'age', 'value': 5}],
        #                                                                   "errors": None, 'links': None}
        #     get_node_relationships_mock.return_value = {"relationships": [
        #         {"start_node": 19, "end_node": id_node,
        #          "name": "hasRegisteredChannel", "id": 0,
        #          "properties": None},
        #         {"start_node": id_node, "end_node": 15,
        #          "name": "hasChannel", "id": 0,
        #          "properties": None},
        #         {"start_node": id_node, "end_node": 16,
        #          "name": "hasRegisteredData", "id": 0,
        #          "properties": None},
        #     ]}
        #     registered_channel = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
        #                                               recordings=[BasicRecordingOut(**{id: 19})],
        #                                               channel=BasicChannelOut(**{id: 15}),
        #                                               registeredData=BasicRegisteredDataOut(**{id: 16}))
        #     registered_channel_service = RegisteredChannelServiceGraphDB()
        #
        #     result = registered_channel_service.delete_registered_channel(id_node)
        #
        #     self.assertEqual(result, registered_channel)
        #     get_node_mock.assert_called_once_with(id_node)
        #     delete_node_mock.assert_called_once_with(id_node)

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
