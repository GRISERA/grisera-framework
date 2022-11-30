import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from models.not_found_model import *
from observable_information.observable_information_model import *
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB


class TestObservableInformationServiceGet(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_observable_information_without_error(self, get_node_relationships_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        observable_information = ObservableInformationOut(id=id_node,
                                                  relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                                 relation_id=0)],
                                                  reversed_relations=[RelationInformation(second_node_id=15,
                                                                                          name="testReversedRelation",
                                                                                          relation_id=0)])
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.get_observable_information(id_node)

        self.assertEqual(result, observable_information)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_observable_information_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.get_observable_information(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_observable_information_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.get_observable_information(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_observable_informations(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1, 'labels': ['Observable Information'],
                                                  'properties': None},
                                                 {'id': 2, 'labels': ['Observable Information'],
                                                  'properties': None
                                                  }]}

        observable_information_one = BasicObservableInformationOut(id=1)
        observable_information_two = BasicObservableInformationOut(id=2)
        observable_informations = ObservableInformationsOut(
            observable_informations=[observable_information_one, observable_information_two])
        observable_informations_service = ObservableInformationServiceGraphDB()

        result = observable_informations_service.get_observable_informations()

        self.assertEqual(result, observable_informations)
        get_nodes_mock.assert_called_once_with("`Observable Information`")

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_observable_informations_empty(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': []}
        observable_informations = ObservableInformationsOut(observable_information=[])
        observable_informations_service = ObservableInformationServiceGraphDB()

        result = observable_informations_service.get_observable_informations()

        self.assertEqual(result, observable_informations)
        get_nodes_mock.assert_called_once_with("`Observable Information`")
