import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from observable_information.observable_information_model import *
from observable_information.observable_information_service import ObservableInformationService


class TestObservableInformationService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_observable_information_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'modality', 'value': 'motion'},
                                                                             {'key': 'live_activity', 'value': 'sound'}],
                                               "errors": None, 'links': None}
        observable_information = ObservableInformationIn(modality='motion', live_activity='sound')
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality='motion', live_activity='sound', id=id_node))
        create_node_mock.assert_called_once_with('`Observable information`')
        create_properties_mock.assert_called_once_with(id_node, observable_information)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_observable_information_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        observable_information = ObservableInformationIn(modality='motion', live_activity='sound')
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality='motion', live_activity='sound', errors=['error']))
        create_node_mock.assert_called_once_with('`Observable information`')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_observable_information_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        observable_information = ObservableInformationIn(modality='motion', live_activity='sound')
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality='motion', live_activity='sound', errors=['error']))
        create_node_mock.assert_called_once_with('`Observable information`')
        create_properties_mock.assert_called_once_with(id_node, observable_information)