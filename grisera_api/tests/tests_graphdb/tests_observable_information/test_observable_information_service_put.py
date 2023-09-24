import unittest
import unittest.mock as mock

from activity.activity_model import BasicActivityOut
from life_activity.life_activity_model import BasicLifeActivityOut
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from modality.modality_model import BasicModalityOut
from modality.modality_service_graphdb import ModalityServiceGraphDB
from observable_information.observable_information_model import *
from models.not_found_model import *

from observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB
from graph_api_service import GraphApiService
from recording.recording_model import BasicRecordingOut
from recording.recording_service_graphdb import RecordingServiceGraphDB
from signal_series.signal_series_model import BasicSignalSeriesOut


class TestObservableInformationServicePut(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'delete_node_properties')
    @mock.patch.object(ModalityServiceGraphDB, 'get_modality')
    @mock.patch.object(LifeActivityServiceGraphDB, 'get_life_activity')
    @mock.patch.object(RecordingServiceGraphDB, 'get_recording')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_update_observable_information_relationships_without_error(self,
                                                                       create_relationships_mock,
                                                                       get_recording_mock,
                                                                       get_life_activity_mock,
                                                                       get_modality_mock,
                                                                       delete_node_properties_mock,
                                                                       get_node_mock, create_properties_mock):
        id_node = 1
        create_properties_mock.return_value = {}
        delete_node_properties_mock.return_value = {}

        get_node_mock.return_value = {'id': id_node, 'labels': ['Observable_Information'],
                                      'properties': None,
                                      "errors": None, 'links': None}
        observable_information_in = ObservableInformationIn(modality_id=6, life_activity_id=7, recording_id=8)
        observable_information_out = BasicObservableInformationOut(id=id_node)
        calls = [mock.call(1)]
        observable_information_service = ObservableInformationServiceGraphDB()

        observable_information_service.modality_service = mock.create_autospec(ModalityServiceGraphDB)
        get_modality_mock.return_value = BasicModalityOut(id=6, modality="HRV")
        observable_information_service.modality_service.get_modality = get_modality_mock

        observable_information_service.life_activity_service = mock.create_autospec(LifeActivityServiceGraphDB)
        get_life_activity_mock.return_value = BasicLifeActivityOut(id=7, life_activity="movement")
        observable_information_service.life_activity_service.get_life_activity = get_life_activity_mock

        observable_information_service.recording_service = mock.create_autospec(RecordingServiceGraphDB)
        get_recording_mock.return_value = BasicRecordingOut(id=8)
        observable_information_service.recording_service.get_recording = get_recording_mock

        result = observable_information_service.update_observable_information_relationships(id_node,
                                                                                            observable_information_in)

        create_relationships_mock.assert_has_calls([mock.call(start_node=id_node, end_node=6, name="hasModality"),
                                                    mock.call(start_node=id_node, end_node=7, name="hasLifeActivity"),
                                                    mock.call(start_node=id_node, end_node=8, name="hasRecording")])
        self.assertEqual(result, observable_information_out)
        get_node_mock.assert_has_calls(calls)
        create_properties_mock.assert_not_called()

    # @mock.patch.object(GraphApiService, 'create_properties')
    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'delete_node_properties')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_update_observable_information_relationships_without_error(self, get_node_relationships_mock,
    #                                                                    delete_node_properties_mock,
    #                                                                    get_node_mock, create_properties_mock):
    #     id_node = 1
    #     create_properties_mock.return_value = {}
    #     delete_node_properties_mock.return_value = {}
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
    #     get_node_mock.return_value = {'id': id_node, 'labels': ['Observable_Information'],
    #                                   'properties': None,
    #                                   "errors": None, 'links': None}
    #     observable_information_in = ObservableInformationIn(modality_id=15, life_activity_id=19)
    #     observable_information_out = ObservableInformationOut(id=id_node, recording=BasicRecordingOut(**{id: 16}),
    #                                                           timeSeries=[BasicSignalSeriesOut(**{id: 19})],
    #                                                           modality=BasicModalityOut(**{id: 15}),
    #                                                           lifeActivity=BasicActivityOut(**{id: 17}))
    #     calls = [mock.call(1)]
    #     observable_information_service = ObservableInformationServiceGraphDB()
    #
    #     result = observable_information_service.update_observable_information_relationships(id_node,
    #                                                                                         observable_information_in)
    #
    #     self.assertEqual(result, observable_information_out)
    #     get_node_mock.assert_has_calls(calls)
    #     create_properties_mock.assert_not_called()
    #     get_node_relationships_mock.assert_has_calls([mock.call(1), mock.call(1)])

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_observable_information_relationships_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        observable_information_in = ObservableInformationIn(modality_id=15, life_activity_id=19)
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.update_observable_information_relationships(id_node,
                                                                                            observable_information_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_update_observable_information_relationships_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        observable_information_in = ObservableInformationIn(modality_id=15, life_activity_id=19)
        observable_information_service = ObservableInformationServiceGraphDB()

        result = observable_information_service.update_observable_information_relationships(id_node,
                                                                                            observable_information_in)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
