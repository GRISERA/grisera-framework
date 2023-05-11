import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from life_activity.life_activity_model import BasicLifeActivityOut
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from modality.modality_model import BasicModalityOut
from modality.modality_service_graphdb import ModalityServiceGraphDB
from observable_information.observable_information_model import *
from observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB
from recording.recording_model import BasicRecordingOut
from recording.recording_service_graphdb import RecordingServiceGraphDB


class TestObservableInformationServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(ModalityServiceGraphDB, 'get_modality')
    @mock.patch.object(LifeActivityServiceGraphDB, 'get_life_activity')
    @mock.patch.object(RecordingServiceGraphDB, 'get_recording')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_observable_information_without_errors(self, create_relationships_mock, get_recording_mock,
                                                        get_life_activity_mock,
                                                        get_modality_mock, get_node_mock, create_node_mock):
        dataset_name = "neo4j"
        id_node = 1
        observable_information_in = ObservableInformationIn(modality_id=6, life_activity_id=7, recording_id=8)
        observable_information_out = BasicObservableInformationOut(id=id_node)

        create_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
                                      'properties': [],
                                      "errors": None, 'links': None}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
                                         'properties': [],
                                         "errors": None, 'links': None}

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

        result = observable_information_service.save_observable_information(observable_information_in, dataset_name)

        create_relationships_mock.assert_has_calls([mock.call(start_node=id_node, end_node=6, name="hasModality",dataset_name=dataset_name),
                 mock.call(start_node=id_node, end_node=7, name="hasLifeActivity",dataset_name=dataset_name),
                 mock.call(start_node=id_node, end_node=8, name="hasRecording",dataset_name=dataset_name)])
        get_node_mock.assert_called_once_with(id_node,dataset_name)
        self.assertEqual(result, observable_information_out)

        @mock.patch.object(GraphApiService, 'create_node')
        def test_save_observable_information_with_node_error(self, create_node_mock):
            dataset_name = "neo4j"
            id_node = 1
            create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
            observable_information = ObservableInformationIn(modality_id=2, life_activity_id=3)
            observable_information_service = ObservableInformationServiceGraphDB()

            result = observable_information_service.save_observable_information(observable_information)

            self.assertEqual(result, ObservableInformationOut(errors=['error']))
            create_node_mock.assert_called_once_with("Observable Information", dataset_name)

# @mock.patch.object(GraphApiService, 'create_node')
# @mock.patch.object(GraphApiService, 'create_properties')
# @mock.patch.object(GraphApiService, 'create_relationships')
# @mock.patch.object(GraphApiService, 'get_node')
# @mock.patch.object(GraphApiService, 'get_node_relationships')
# def test_save_observable_information_without_errors(self, get_node_relationships_mock, get_node_mock,
#                                                     create_relationships_mock, create_properties_mock,
#                                                     create_node_mock):
#     id_node = 1
#     get_node_mock.return_value = {'id': id_node, 'labels': ['Observable Information'],
#                                   'properties': None,
#                                   "errors": None, 'links': None}
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
#     create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
#     create_properties_mock.return_value = {'id': id_node, 'errors': None, 'links': None}
#     create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
#                                               'name': 'hasActivityExecution', 'errors': None}
#
#     observable_information_in = ObservableInformationIn(modality_id=2, life_activity_id=3)
#     observable_information_out = ObservableInformationOut(id=id_node, recording=BasicRecordingOut(**{id: 16}),
#                                                           timeSeries=[BasicTimeSeriesOut(**{id: 19})],
#                                                           modality=BasicModalityOut(**{id: 15}),
#                                                           lifeActivity=BasicActivityOut(**{id: 17}))
#     calls = [mock.call(2), mock.call(3), mock.call(1)]
#     observable_information_service = ObservableInformationServiceGraphDB()
#
#     result = observable_information_service.save_observable_information(observable_information_in)
#
#     self.assertEqual(result, observable_information_out)
#     create_node_mock.assert_called_once_with("`Observable Information`")
#     # create_properties_mock.assert_not_called()
#     create_relationships_mock.assert_not_called()
#     get_node_mock.assert_has_calls(calls)
