import unittest
import unittest.mock as mock

from arrangement.arrangement_model import *
from arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from graph_api_service import GraphApiService


class TestArrangementServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_arrangement_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'arrangement_type',
                                                                              'value': 'personal two persons'},
                                                                             {'key': 'arrangement_distance',
                                                                              'value': 'intimate zone'}],
                                               "errors": None, 'links': None}
        arrangement = ArrangementIn(arrangement_type='personal two persons', arrangement_distance='intimate zone')
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.save_arrangement(arrangement)

        self.assertEqual(result, ArrangementOut(id=id_node, arrangement_type='personal two persons',
                                                arrangement_distance='intimate zone'))
        create_node_mock.assert_called_once_with('Arrangement')
        create_properties_mock.assert_called_once_with(id_node, arrangement)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_arrangement_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        arrangement = ArrangementIn(arrangement_type='personal two persons', arrangement_distance='intimate zone')
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.save_arrangement(arrangement)

        self.assertEqual(result, ArrangementOut(arrangement_type='personal two persons',
                                                arrangement_distance='intimate zone', errors=['error']))
        create_node_mock.assert_called_once_with('Arrangement')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_arrangement_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        arrangement = ArrangementIn(arrangement_type='personal two persons', arrangement_distance='intimate zone')
        arrangement_service = ArrangementServiceGraphDB()

        result = arrangement_service.save_arrangement(arrangement)

        self.assertEqual(result, ArrangementOut(arrangement_type='personal two persons',
                                                arrangement_distance='intimate zone', errors=['error']))
        create_node_mock.assert_called_once_with('Arrangement')
        create_properties_mock.assert_called_once_with(id_node, arrangement)

    # @mock.patch.object(GraphApiService, 'get_nodes')
    # def test_get_arrangements_without_error(self, get_nodes_mock):
    #     get_nodes_mock.return_value = {'nodes': [{'id': 1,
    #                                               'properties': [{'key': 'arrangement_type', 'value': 'personal two persons'},
    #                                                              {'key': 'arrangement_distance', 'value': 'intimate zone'}]},
    #                                              {'id': 2,
    #                                               'properties': [{'key': 'arrangement_type', 'value': 'personal two persons'},
    #                                                              {'key': 'arrangement_distance', 'value': 'intimate zone'}]}
    #                                              ],
    #                                    "errors": None, 'links': None}
    #     arrangement_service = ArrangementServiceGraphDB()
    #
    #     result = arrangement_service.get_arrangements()
    #
    #     get_nodes_mock.assert_called_once_with('Arrangement')
    #     self.assertEqual(result, ArrangementsOut(arrangements=[BasicArrangementOut(id=1, arrangement_type='personal two persons'),
    #                                                        BasicArrangementOut(id=2, arrangement_type='personal two persons')]))
    #
    # @mock.patch.object(GraphApiService, 'get_nodes')
    # def test_get_arrangements_with_error(self, get_nodes_mock):
    #     get_nodes_mock.return_value = {'nodes': None, "errors": ['error'], 'links': None}
    #     arrangement_service = ArrangementServiceGraphDB()
    #
    #     result = arrangement_service.get_arrangements()
    #
    #     get_nodes_mock.assert_called_once_with('Arrangement')
    #     self.assertEqual(result, ArrangementsOut(errors=['error']))
