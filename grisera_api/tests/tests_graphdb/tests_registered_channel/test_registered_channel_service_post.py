import unittest
import unittest.mock as mock

from channel.channel_model import BasicChannelOut
from channel.channel_service_graphdb import ChannelServiceGraphDB
from graph_api_service import GraphApiService
from registered_channel.registered_channel_model import *
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from registered_data.registered_data_model import BasicRegisteredDataOut
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB


class TestRegisteredChannelServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(ChannelServiceGraphDB, 'get_channel')
    @mock.patch.object(RegisteredDataServiceGraphDB, 'get_registered_data')
    def test_save_registered_channel_without_errors(self, get_registered_data_mock,
                                                    get_channel_mock, get_node_mock, create_relationships_mock, create_node_mock):
        dataset_name = "neo4j"
        registered_channel_in = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        get_channel_mock.return_value = BasicChannelOut(**{'id': 2, 'type': 'Audio'})
        get_registered_data_mock.return_value = BasicRegisteredDataOut(**{'id': 3, 'source': 'test'})
        get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
                                      'properties': [],
                                      "errors": None, 'links': None}

        registered_channel_out = BasicRegisteredChannelOut(age=5, id=id_node, additional_properties=[])
        registered_channel_service = RegisteredChannelServiceGraphDB()
        registered_channel_service.channel_service = mock.create_autospec(ChannelServiceGraphDB)

        registered_channel_service.channel_service.get_channel = get_channel_mock
        registered_channel_service.registered_data_service = mock.create_autospec(RegisteredDataServiceGraphDB)
        registered_channel_service.registered_data_service.get_registered_data = get_registered_data_mock

        result = registered_channel_service.save_registered_channel(registered_channel_in, dataset_name)

        self.assertEqual(result, registered_channel_out)
        create_node_mock.assert_called_once_with('Registered Channel', dataset_name)
        create_relationships_mock.assert_has_calls([
            mock.call(start_node=id_node, end_node=2, name='hasChannel',dataset_name=dataset_name),
            mock.call(start_node=id_node, end_node=3, name='hasRegisteredData',dataset_name=dataset_name)
        ])
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    # @mock.patch.object(GraphApiService, 'create_node')
    # @mock.patch.object(GraphApiService, 'create_properties')
    # @mock.patch.object(GraphApiService, 'create_relationships')
    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_save_registered_channel_without_errors(self, get_node_relationships_mock, get_node_mock,
    #                                                 create_relationships_mock, create_properties_mock,
    #                                                 create_node_mock):
    #     id_node = 1
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Registered Channel'],
    #                                   'properties': [],
    #                                   "errors": None, 'links': None}
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
    #     create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
    #     create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
    #     create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
    #                                               'name': 'hasParticipant', 'errors': None}
    #     registered_channel_in = RegisteredChannelIn(channel_id=2, registered_data_id=3)
    #     registered_channel_out = RegisteredChannelOut(age=5, id=id_node, additional_properties=[],
    #                                                   recordings=[BasicRecordingOut(**{id: 19})],
    #                                                   channel=BasicChannelOut(**{id: 15}),
    #                                                   registeredData=BasicRegisteredDataOut(**{id: 16}))
    #     calls = [mock.call(2), mock.call(3), mock.call(1)]
    #     registered_channel_service = RegisteredChannelServiceGraphDB()
    #
    #     result = registered_channel_service.save_registered_channel(registered_channel_in)
    #
    #     self.assertEqual(result, registered_channel_out)
    #     create_node_mock.assert_called_once_with('`Registered Channel`')
    #     create_properties_mock.assert_not_called()
    #     create_relationships_mock.assert_not_called()
    #     get_node_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_registered_channel_with_node_error(self, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        registered_channel = RegisteredChannelIn(channel_id=2, registered_data_id=3)
        registered_channel_service = RegisteredChannelServiceGraphDB()

        result = registered_channel_service.save_registered_channel(registered_channel, dataset_name)

        self.assertEqual(result, RegisteredChannelOut(errors=['error']))
        create_node_mock.assert_called_once_with('Registered Channel', dataset_name)
