import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from models.not_found_model import *
from signal_series.signal_series_model import *
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from time_series.time_series_service_graphdb_with_signal_values import TimeSeriesServiceGraphDBWithSignalValues


class TestTimeSeriesWithSignalValuesServiceDelete(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'delete_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(TimeSeriesServiceGraphDB, 'delete_signal_series')
    def test_delete_signal_series_without_error(self, delete_signal_series_mock, create_relationships_mock,
                                              get_node_relationships_mock, delete_node_mock):
        time_series = SignalSeriesOut(id=10, type="Timestamp", source="cos",
                                    signal_values=[
                                        {
                                            'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                                             'properties': [{'key': 'value', 'value': '10'}]},
                                            'timestamp': {'labels': ['Timestamp'], 'id': 1, 'properties': [
                                                {'key': 'timestamp', 'value': '100'}]}
                                        },
                                        {
                                            'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                                             'properties': [
                                                                 {'key': 'value', 'value': '20'}]},
                                            'timestamp': {'labels': ['Timestamp'], 'id': 3, 'properties': [
                                                {'key': 'timestamp', 'value': '200'}]}
                                        },
                                        {
                                            'signal_value': {'labels': ['Signal Value'], 'id': 6,
                                                             'properties': [
                                                                 {'key': 'value', 'value': '30'}]},
                                            'timestamp': {'labels': ['Timestamp'], 'id': 5, 'properties': [
                                                {'key': 'timestamp', 'value': '300'}]}
                                        },
                                        {
                                            'signal_value': {'labels': ['Signal Value'], 'id': 8,
                                                             'properties': [
                                                                 {'key': 'value', 'value': '40'}]},
                                            'timestamp': {'labels': ['Timestamp'], 'id': 7, 'properties': [
                                                {'key': 'timestamp', 'value': '400'}]}
                                        }
                                    ])
        delete_signal_series_mock.return_value = time_series

        def get_node_relationships_side_effect(*args):
            if args[0] == 1:
                return {"relationships": [
                    {"start_node": 20, "end_node": 1,
                     "name": "takes", "id": 100,
                     "properties": None},
                    {"start_node": 1, "end_node": 3,
                     "name": "next", "id": 101,
                     "properties": None}]}
            elif args[0] == 3:
                return {"relationships": [
                    {"start_node": 20, "end_node": 3,
                     "name": "takes", "id": 102,
                     "properties": None},
                    {"start_node": 3, "end_node": 30,
                     "name": "startInSec", "id": 103,
                     "properties": None},
                    {"start_node": 1, "end_node": 3,
                     "name": "next", "id": 101,
                     "properties": None},
                    {"start_node": 3, "end_node": 5,
                     "name": "next", "id": 104,
                     "properties": None}]}
            elif args[0] == 5:
                return {"relationships": [
                    {"start_node": 3, "end_node": 5,
                     "name": "next", "id": 104,
                     "properties": None},
                    {"start_node": 5, "end_node": 7,
                     "name": "next", "id": 105,
                     "properties": None}]}
            elif args[0] == 7:
                return {"relationships": [
                    {"start_node": 5, "end_node": 7,
                     "name": "next", "id": 105,
                     "properties": None},
                    {"start_node": 7, "end_node": 30,
                     "name": "endInSec", "id": 106,
                     "properties": None}]}

        get_node_relationships_mock.side_effect = get_node_relationships_side_effect
        time_series_service = TimeSeriesServiceGraphDBWithSignalValues()

        result = time_series_service.delete_signal_series(10)

        self.assertEqual(time_series, result)
        self.assertEqual([
            mock.call(2),
            mock.call(4),
            mock.call(6),
            mock.call(8),
            mock.call(1),
            mock.call(5),
        ], delete_node_mock.call_args_list)
        self.assertEqual([
            mock.call(start_node=20, end_node=3, name='takes'),
            mock.call(start_node=3, end_node=7, name='next')
        ], create_relationships_mock.call_args_list)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_delete_signal_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        time_series_service = TimeSeriesServiceGraphDBWithSignalValues()

        result = time_series_service.delete_signal_series(id_node)

        self.assertEqual(not_found, result)
        get_node_mock.assert_called_once_with(id_node)
