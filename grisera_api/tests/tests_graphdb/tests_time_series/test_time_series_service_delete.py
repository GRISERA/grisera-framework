import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut
from observable_information.observable_information_model import BasicObservableInformationOut
from signal_series.signal_series_model import *
from models.not_found_model import *

from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from graph_api_service import GraphApiService


class TestTimeSeriesServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_without_error(self, get_node_mock, delete_node_mock):
        id_node = 1
        delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Time_Series'],
                                                                      'properties': [{'key': 'type', 'value': "Epoch"},
                                                                                     {'key': 'source', 'value': "cos"}],
                                                                      "errors": None, 'links': None}
        time_series = BasicSignalSeriesOut(id=1, type="Epoch", source="cos", additional_properties=[])
        time_series_service = TimeSeriesServiceGraphDB()

        result = time_series_service.delete_signal_series(id_node)

        self.assertEqual(result, time_series)
        get_node_mock.assert_called_once_with(id_node)
        delete_node_mock.assert_called_once_with(id_node)

    # @mock.patch.object(GraphApiService, 'delete_node')
    # @mock.patch.object(GraphApiService, 'get_node')
    # @mock.patch.object(GraphApiService, 'get_node_relationships')
    # def test_delete_signal_series_without_error(self, get_node_relationships_mock, get_node_mock, delete_node_mock):
    #     id_node = 1
    #     delete_node_mock.return_value = get_node_mock.return_value = {'id': id_node, 'labels': ['Time_Series'],
    #                                                                   'properties': [{'key': 'type', 'value': "Epoch"},
    #                                                                                  {'key': 'source', 'value': "cos"}],
    #                                                                   "errors": None, 'links': None}
    #     get_node_relationships_mock.return_value = {"relationships": [
    #         {"start_node": id_node, "end_node": 19,
    #          "name": "hasObservableInformation", "id": 0,
    #          "properties": None},
    #         {"start_node": id_node, "end_node": 15,
    #          "name": "hasMeasure", "id": 0,
    #          "properties": None}]}
    #     time_series = SignalSeriesOut(id=1, type="Epoch", source="cos", additional_properties=[],
    #                                 observable_informations=[BasicObservableInformationOut(**{id: 19})],
    #                                 measure=BasicMeasureOut(**{id: 15}))
    #     time_series_service = TimeSeriesServiceGraphDB()
    #
    #     result = time_series_service.delete_signal_series(id_node)
    #
    #     self.assertEqual(result, time_series)
    #     get_node_mock.assert_called_once_with(id_node)
    #     delete_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_without_label(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Test'], 'properties': None,
                                      "errors": None, 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors="Node not found.")
        time_series_service = TimeSeriesServiceGraphDB()

        result = time_series_service.delete_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        time_series_service = TimeSeriesServiceGraphDB()

        result = time_series_service.delete_signal_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
