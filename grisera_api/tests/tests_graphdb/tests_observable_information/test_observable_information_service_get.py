import unittest
import unittest.mock as mock

from activity.activity_model import BasicActivityOut
from graph_api_service import GraphApiService
from life_activity.life_activity_model import BasicLifeActivityOut
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from modality.modality_model import BasicModalityOut
from modality.modality_service_graphdb import ModalityServiceGraphDB
from models.not_found_model import *
from observable_information.observable_information_model import *
from observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB
from recording.recording_model import BasicRecordingOut
from recording.recording_service_graphdb import RecordingServiceGraphDB
from time_series.time_series_model import BasicTimeSeriesOut


class TestObservableInformationServiceGet(unittest.TestCase):

    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(ModalityServiceGraphDB, 'get_modality')
    # @mock.patch.object(LifeActivityServiceGraphDB, 'get_life_activity')
    # @mock.patch.object(RecordingServiceGraphDB, 'get_recording')
    # @mock.patch.object(GraphApiService, 'create_relationships')
    # def test_get_observable_information_without_error(self, create_relationships_mock, get_recording_mock,
    #                                                   get_life_activity_mock,
    #                                                   get_modality_mock, get_node_mock):
    #     id_node = 1
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
    #                                   'properties': [],
    #                                   "errors": None, 'links': None}
    #
    #     observable_information = BasicObservableInformationOut(id=id_node)
    #
    #     observable_information_service = ObservableInformationServiceGraphDB()
    #
    #     observable_information_service.modality_service = mock.create_autospec(ModalityServiceGraphDB)
    #     get_modality_mock.return_value = BasicModalityOut(id=6, modality="HRV")
    #     observable_information_service.modality_service.get_modality = get_modality_mock
    #
    #     observable_information_service.life_activity_service = mock.create_autospec(LifeActivityServiceGraphDB)
    #     get_life_activity_mock.return_value = BasicLifeActivityOut(id=7, life_activity="movement")
    #     observable_information_service.life_activity_service.get_life_activity = get_life_activity_mock
    #
    #     observable_information_service.recording_service = mock.create_autospec(RecordingServiceGraphDB)
    #     get_recording_mock.return_value = BasicRecordingOut(id=8)
    #     observable_information_service.recording_service.get_recording = get_recording_mock
    #
    #     result = observable_information_service.get_observable_information(id_node)
    #     calls = [mock.call(start_node=id_node, end_node=6, name="hasModality"),
    #              mock.call(start_node=id_node, end_node=7, name="hasLifeActivity"),
    #              mock.call(start_node=id_node, end_node=8, name="hasRecording")]
    #
    #     create_relationships_mock.assert_has_calls(calls)
    #     self.assertEqual(result, observable_information)
    #     get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_observable_information_without_error(self, get_node_relationships_mock, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        observable_information = BasicObservableInformationOut(id=id_node)
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.get_observable_information(id_node, dataset_name)

        self.assertEqual(result, observable_information)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_observable_information_without_label(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.get_observable_information(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_observable_information_with_error(self, get_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.get_observable_information(id_node, dataset_name)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node, dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_observable_informations(self, get_nodes_mock):
        dataset_name = "neo4j"
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

        result = observable_informations_service.get_observable_informations(dataset_name)

        self.assertEqual(result, observable_informations)
        get_nodes_mock.assert_called_once_with("`Observable Information`", dataset_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_observable_informations_empty(self, get_nodes_mock):
        dataset_name = "neo4j"
        get_nodes_mock.return_value = {'nodes': []}
        observable_informations = ObservableInformationsOut(observable_information=[])
        observable_informations_service = ObservableInformationServiceGraphDB()

        result = observable_informations_service.get_observable_informations(dataset_name)

        self.assertEqual(result, observable_informations)
        get_nodes_mock.assert_called_once_with("`Observable Information`", dataset_name)
