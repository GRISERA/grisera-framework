import unittest
import unittest.mock as mock

from channel.channel_model import BasicChannelOut
from channel.channel_service_graphdb import ChannelServiceGraphDB
from recording.recording_model import BasicRecordingOut
from registered_channel.registered_channel_model import *
from models.not_found_model import *

from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from graph_api_service import GraphApiService
from registered_data.registered_data_model import BasicRegisteredDataOut
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredChannelServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ChannelServiceGraphDB, 'get_channel')
    @mock.patch.object(RegisteredDataServiceGraphDB, 'get_registered_data')
    def test_update_registered_channel_relationships_without_error(self, get_registered_data_mock, get_channel_mock,
                                                                   create_relationships_mock,
                                                                   delete_node_properties_mock,
                                                                   get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
                                      'properties': [{'key': 'age', 'value': 5}, {'key': 'identifier', 'value': 5}],
                                      "errors": None, 'links': None}
        registered_channel_in = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        calls = [mock.call(1)]

        registered_channel_out = BasicRegisteredChannelOut(age=5, id=id_node)

        registered_channel_service = RegisteredChannelServiceGraphDB()
        registered_channel_service.channel_service = mock.create_autospec(ChannelServiceGraphDB)
        registered_channel_service.channel_service.get_channel = get_channel_mock

        registered_channel_service.registered_data_service = mock.create_autospec(RegisteredDataServiceGraphDB)
        registered_channel_service.registered_data_service.get_registered_data = get_registered_data_mock

        result = registered_channel_service.update_registered_channel_relationships(id_node, registered_channel_in)

        self.assertEqual(result, registered_channel_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_not_called()
        create_relationships_mock.assert_has_calls([
            mock.call(start_node=id_node, end_node=2, name='hasChannel'),
            mock.call(start_node=id_node, end_node=3, name='hasRegisteredData')
        ])

        # @mock.patch.object(GraphApiService, 'create_properties')
        # @mock.patch.object(GraphApiService, 'get_node')
        # @mock.patch.object(GraphApiService, 'delete_node_properties')
        # @mock.patch.object(GraphApiService, 'get_node_relationships')
        # def test_update_registered_channel_relationships_without_error(self, get_node_relationships_mock,
        #                                                                delete_node_properties_mock,
        #                                                                get_node_mock, create_properties_mock):
        #     id_node = 1
        #     create_properties_mock.return_value = {}
        #     delete_node_properties_mock.return_value = {}
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
        #     get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
        #                                   'properties': [{'key': 'age', 'value': 5}, {'key': 'identifier', 'value': 5}],
        #                                   "errors": None, 'links': None}
        #     registered_channel_in = RegisteredChannelIn(channel_id=15, registered_data_id=19)
        #     registered_channel_out = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
        #                                                   recordings=[BasicRecordingOut(**{id: 19})],
        #                                                   channel=BasicChannelOut(**{id: 15}),
        #                                                   registeredData=BasicRegisteredDataOut(**{id: 16}))
        #     calls = [mock.call(1)]
        #     registered_channel_service = RegisteredChannelServiceGraphDB()
        #
        #     result = registered_channel_service.update_registered_channel_relationships(id_node, registered_channel_in)
        #
        #     self.assertEqual(result, registered_channel_out)
        #     get_node_mock.assert_has_calls(calls)
        #     create_properties_mock.assert_not_called()
        #     get_node_relationships_mock.assert_has_calls([mock.call(1), mock.call(1)])

    # class TestRegisteredChannelServicePut(unittest.TestCase):
    #
    #     @mock.patch.object(GraphApiService, 'create_properties')
    #     @mock.patch.object(GraphApiService, 'get_node')
    #     @mock.patch.object(GraphApiService, 'delete_node_properties')
    #     @mock.patch.object(GraphApiService, 'get_node_relationships')
    #     def test_update_registered_channel_relationships_without_error(self, get_node_relationships_mock,
    #                                                                    delete_node_properties_mock,
    #                                                                    get_node_mock, create_properties_mock):
    #         id_node = 1
    #         create_properties_mock.return_value = {}
    #         delete_node_properties_mock.return_value = {}
    #         get_node_relationships_mock.return_value = {"relationships": [
    #             {"start_node": 19, "end_node": id_node,
    #              "name": "hasRegisteredChannel", "id": 0,
    #              "properties": None},
    #             {"start_node": id_node, "end_node": 15,
    #              "name": "hasChannel", "id": 0,
    #              "properties": None},
    #             {"start_node": id_node, "end_node": 16,
    #              "name": "hasRegisteredData", "id": 0,
    #              "properties": None},
    #         ]}
    #         get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
    #                                       'properties': [{'key': 'age', 'value': 5}, {'key': 'identifier', 'value': 5}],
    #                                       "errors": None, 'links': None}
    #         registered_channel_in = RegisteredChannelIn(channel_id=15, registered_data_id=19)
    #         registered_channel_out = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
    #                                                       recordings=[BasicRecordingOut(**{id: 19})],
    #                                                       channel=BasicChannelOut(**{id: 15}),
    #                                                       registeredData=BasicRegisteredDataOut(**{id: 16}))
    #         calls = [mock.call(1)]
    #         registered_channel_service = RegisteredChannelServiceGraphDB()
    #
    #         result = registered_channel_service.update_registered_channel_relationships(id_node, registered_channel_in)
    #
    #         self.assertEqual(result, registered_channel_out)
    #         get_node_mock.assert_has_calls(calls)
    #         create_properties_mock.assert_not_called()
    #         get_node_relationships_mock.assert_has_calls([mock.call(1), mock.call(1)])


    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_registered_channel_relationships_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        registered_channel_in = RegisteredChannelIn(channel_id=15, registered_data_id=19)
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.update_registered_channel_relationships(id_node, registered_channel_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_registered_channel_relationships_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        registered_channel_in = RegisteredChannelIn(channel_id=15, registered_data_id=19)
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.update_registered_channel_relationships(id_node, registered_channel_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
