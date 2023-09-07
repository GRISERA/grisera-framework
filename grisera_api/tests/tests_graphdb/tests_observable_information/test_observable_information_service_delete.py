import unittest
import unittest.mock as mock

from activity.activity_model import BasicActivityOut
from graph_api_service import GraphApiService
from modality.modality_model import BasicModalityOut
from models.not_found_model import *
from observable_information.observable_information_model import *
from observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB
from recording.recording_model import BasicRecordingOut
from time_series.time_series_model import BasicTimeSeriesOut


class TestObservableInformationServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_observable_information_without_error(self, get_node_mock,
                                                         delete_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node,
                                                                      'labels': ['Observable Information'],
                                                                      'properties': None,
                                                                      "errors": None, 'links': None}
        observable_information = BasicObservableInformationOut(id=id_node)
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.delete_observable_information(id_node, dataset_name)

        self.assertEqual(result, observable_information)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
        delete_node_mock.assert_called_once_with(id_node, dataset_name)

    # @mock.patch.object(GraphApiService, 'delete_node')
    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_delete_observable_information_without_error(self, get_node_relationships_mock, get_node_mock,
    #                                                      delete_node_mock):
    #     id_node = 1
    #     delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node,
    #                                                                   'labels': ['Observable Information'],
    #                                                                   'properties': None,
    #                                                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": 19, "end_node": id_node,
    #          "name": "hasObservableInformation", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 15,
    #          "name": "hasModality", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 16,
    #          "name": "hasRecording", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 17,
    #          "name": "hasLifeActivity", "id": 0,
    #          "properties": None},
    #     ]}
    #     observable_information = ObservableInformationOut(id=id_node, recording=BasicRecordingOut(**{id: 16}),
    #                                                       timeSeries=[BasicTimeSeriesOut(**{id: 19})],
    #                                                       modality=BasicModalityOut(**{id: 15}),
    #                                                       lifeActivity=BasicActivityOut(**{id: 17}))
    #     observable_information_service = ObservableInformationServiceGraphDB()
    #
    #     result = observable_information_service.delete_observable_information(id_node)
    #
    #     self.assertEqual(result, observable_information)
    #     get_node_mock.assert_called_once_with(id_node)
    #     delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_observable_information_without_participant_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.delete_observable_information(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_observable_information_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.delete_observable_information(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)
