import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut
from observable_information.observable_information_service import ObservableInformationService

from modality.modality_service import ModalityService
from modality.modality_model import ModalitiesOut, BasicModalityOut
from live_activity.live_activity_service import LiveActivityService
from live_activity.live_activity_model import LiveActivitiesOut, BasicLiveActivityOut


class TestObservableInformationService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ModalityService, 'get_modalities')
    @mock.patch.object(LiveActivityService, 'get_live_activities')
    def test_save_observable_information_without_error(self, get_live_activities_mock, get_modalities_mock,
                                                       create_relationships_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_relationships_mock.return_value = {'id': 3, 'start_node': 2, "errors": None, 'links': None}

        get_modalities_mock.return_value = ModalitiesOut(modalities=[BasicModalityOut(id=4, modality='motion')])
        get_live_activities_mock.return_value = \
            LiveActivitiesOut(live_activities=[BasicLiveActivityOut(id=5, live_activity='sound')])
        calls = [mock.call(start_node=id_node, end_node=4, name="hasModality"),
                 mock.call(start_node=id_node, end_node=5, name="hasLiveActivity")]

        observable_information = ObservableInformationIn(modality='motion', live_activity='sound')
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality='motion', live_activity='sound', id=id_node))
        create_node_mock.assert_called_once_with('`Observable information`')
        get_modalities_mock.assert_called_once()
        get_live_activities_mock.assert_called_once()
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_observable_information_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        observable_information = ObservableInformationIn(modality='motion', live_activity='sound')
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality='motion', live_activity='sound', errors=['error']))
        create_node_mock.assert_called_once_with('`Observable information`')

