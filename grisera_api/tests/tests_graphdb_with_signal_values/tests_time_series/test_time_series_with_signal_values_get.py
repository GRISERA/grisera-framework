import unittest
from unittest import mock

from graph_api_service import GraphApiService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from property.property_model import PropertyIn
from time_series.time_series_model import TimeSeriesOut
from time_series.time_series_service_graphdb_with_signal_values import TimeSeriesServiceGraphDBWithSignalValues


class TestTimeSeriesWithSignalValuesServicePost(unittest.TestCase):
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_nodes_by_query')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_get_time_series_without_error(self, get_node_relationships_mock, get_nodes_by_query_mock, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'labels': ['Time Series'],
                                      'properties': [{'key': 'type', 'value': "Timestamp"},
                                                     {'key': 'source', 'value': "cos"},
                                                     {'key': 'test', 'value': 'test2'}],
                                      "errors": None, 'links': None}
        get_nodes_by_query_mock.return_value = {
            'rows': [
                [{'labels': ['Signal Value'], 'id': 2, 'properties': [{'key': 'value', 'value': '10'}]},
                 {'labels': ['Timestamp'], 'id': 1, 'properties': [{'key': 'timestamp', 'value': '100'}]}],
                [{'labels': ['Signal Value'], 'id': 4, 'properties': [{'key': 'value', 'value': '20'}]},
                 {'labels': ['Timestamp'], 'id': 3, 'properties': [{'key': 'timestamp', 'value': '200'}]}],
                [{'labels': ['Signal Value'], 'id': 6, 'properties': [{'key': 'value', 'value': '30'}]},
                 {'labels': ['Timestamp'], 'id': 5, 'properties': [{'key': 'timestamp', 'value': '300'}]}]
            ],
            'errors': []
        }
        get_node_relationships_mock.return_value = {"relationships": [
            {"start_node": id_node, "end_node": 19,
             "name": "testRelation", "id": 0,
             "properties": None},
            {"start_node": 15, "end_node": id_node,
             "name": "testReversedRelation", "id": 0,
             "properties": None}]}
        additional_properties = [PropertyIn(key='test', value='test2')]
        time_series = TimeSeriesOut(id=1, type="Timestamp", source="cos",
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
                                        }
                                    ],
                                    additional_properties=additional_properties,
                                    relations=[RelationInformation(second_node_id=19, name="testRelation",
                                                                   relation_id=0)],
                                    reversed_relations=[RelationInformation(second_node_id=15,
                                                                            name="testReversedRelation",
                                                                            relation_id=0)])
        time_series_service = TimeSeriesServiceGraphDBWithSignalValues()

        result = time_series_service.get_time_series(id_node)

        self.assertEqual(time_series, result)
        get_node_mock.assert_called_once_with(id_node)
        get_node_relationships_mock.assert_called_once_with(id_node)

    @mock.patch.object(GraphApiService, 'get_node')
    def test_get_time_series_with_error(self, get_node_mock):
        id_node = 1
        get_node_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        not_found = NotFoundByIdModel(id=id_node, errors=['error'])
        time_series_service = TimeSeriesServiceGraphDBWithSignalValues()

        result = time_series_service.get_time_series(id_node)

        self.assertEqual(result, not_found)
        get_node_mock.assert_called_once_with(id_node)
