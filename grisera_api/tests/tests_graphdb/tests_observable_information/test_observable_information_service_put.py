import unittest
import unittest.mock as mock

from observable_information.observable_information_model import *
from models.not_found_model import *

from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB
from graph_api_service import GraphApiService


class TestObservableInformationServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_update_observable_information_relationships_without_error(self, get_node_relationships_mock, delete_node_properties_mock,
                                                    get_node_mock, create_properties_mock):
        database_name = "neo4j"
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}
        get_node_relationships_mock.return_value = {"relationships": [
                                                    {"start_node": id_node, "end_node": 19,
                                                     "name": "testRelation", "id": 0,
                                                     "properties": None},
                                                    {"start_node": 15, "end_node": id_node,
                                                     "name": "testReversedRelation", "id": 0,
                                                     "properties": None}]}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
                                      'properties': None,
                                      "errors": None, 'links': None}
        observable_information_in = ObservableInformationIn(modality_id=15, life_activity_id=19)
        observable_information_out = ObservableInformationOut(id=id_node, relations=
                                 [RelationInformation(second_node_id=19, name="testRelation", relation_id=0)],
                                                    reversed_relations=
                                 [RelationInformation(second_node_id=15, name="testReversedRelation", relation_id=0)])
        calls = [mock.call(1, database_name)]
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.update_observable_information_relationships(id_node, observable_information_in, database_name)

        self.assertEqual(result, observable_information_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_not_called()
        get_node_relationships_mock.assert_has_calls([mock.call(1, database_name), mock.call(1, database_name)])

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_observable_information_relationships_without_label(self, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        observable_information_in = ObservableInformationIn(modality_id=15, life_activity_id=19)
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.update_observable_information_relationships(id_node, observable_information_in, database_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, database_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_observable_information_relationships_with_error(self, get_node_mock):
        database_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        observable_information_in = ObservableInformationIn(modality_id=15, life_activity_id=19)
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.update_observable_information_relationships(id_node, observable_information_in, database_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, database_name)
