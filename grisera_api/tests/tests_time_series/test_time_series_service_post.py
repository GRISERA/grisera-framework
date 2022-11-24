import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from time_series.time_series_model import *
from time_series.time_series_service import TimeSeriesService


def relationship_function(*args, **kwargs):
    if kwargs['name'] == 'hasPublication':
        return {'start_node': 1, 'end_node': 3, 'id': 5, 'name': 'hasPublication', 'errors': ['error']}
    return {'start_node': 1, 'end_node': 2, 'id': 4, 'name': 'hasAuthor', 'errors': None}


class TestTimeSeriesServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'get_node')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    def test_save_time_series_without_errors(self, get_node_relationships_mock, get_node_mock,
                                             create_relationships_mock, create_properties_mock, create_node_mock):

        time_series_id = 1
        experiment_id = 23
        timestamp_id = 34
        signal_value_id = 35
        observable_information_id = 2
        measure_id = 3

        def get_node_relationships_side_effect(*args, **kwargs):
            if args[0] == time_series_id:
                return {"relationships": [
                    {"start_node": time_series_id, "end_node": 19,
                     "name": "testRelation", "id": 0,
                     "properties": None},
                    {"start_node": 15, "end_node": time_series_id,
                     "name": "testReversedRelation", "id": 0,
                     "properties": None}]}
            elif args[0] == experiment_id:
                return {"relationships": []}
            elif args[0] == timestamp_id:
                return {"relationships": []}
            else:
                return None

        def create_node_side_effect(*args, **kwargs):
            if args[0] == "`Time Series`":
                return {'id': time_series_id, 'properties': None, "errors": None, 'links': None}
            elif args[0] == "`Timestamp`":
                return {'id': timestamp_id, 'properties': [{"key": "timestamp", "value": 100}], "errors": None,
                        'links': None}
            elif args[0] == "`Signal Value`":
                return {'id': signal_value_id, 'properties': [{"key": "timestamp", "value": 100}], "errors": None,
                        'links': None}
            else:
                return None

        def get_node_side_effect(*args, **kwargs):
            if args[0] == time_series_id:
                return {'id': time_series_id, 'labels': ['Time Series'],
                        'properties': [{'key': 'type', 'value': "Epoch"},
                                       {'key': 'source', 'value': "cos"}],
                        "errors": None, 'links': None}
            elif args[0] == observable_information_id:
                return {'id': observable_information_id, 'labels': ['Time Series'],
                        'properties': [{'key': 'type', 'value': "Epoch"},
                                       {'key': 'source', 'value': "cos"}],
                        "errors": None, 'links': None}
            elif args[0] == measure_id:
                return {'id': measure_id, 'labels': ['Time Series'],
                        'properties': [{'key': 'type', 'value': "Epoch"},
                                       {'key': 'source', 'value': "cos"}],
                        "errors": None, 'links': None}
            elif args[0] == timestamp_id:
                return {'id': timestamp_id, 'properties': [{"key": "timestamp", "value": 100}], "errors": None,
                        'links': None}
            else:
                return None

        def create_properties_side_effect(*args, **kwargs):
            return {'id': args[0], 'errors': None, 'links': None}

        get_node_relationships_mock.side_effect = get_node_relationships_side_effect
        create_node_mock.side_effect = create_node_side_effect
        create_properties_mock.side_effect = create_properties_side_effect
        get_node_mock.side_effect = get_node_side_effect
        create_relationships_mock.return_value = {'start_node': 1, 'end_node': 2,
                                                  'name': 'hasMeasure', 'errors': None}
        time_series_in = TimeSeriesIn(id=1, type="Epoch", source="cos",
                                      observable_information_id=observable_information_id, measure_id=measure_id,
                                      signal_values=[SignalIn(value=10, start_timestamp=100, end_timestamp=150),
                                                     SignalIn(value=20, start_timestamp=200, end_timestamp=250)])
        time_series_out = TimeSeriesOut(id=1, type="Epoch", source="cos", additional_properties=[],
                                        relations=
                                        [RelationInformation(second_node_id=19, name="testRelation",
                                                             relation_id=0)],
                                        reversed_relations=
                                        [RelationInformation(second_node_id=15, name="testReversedRelation",
                                                             relation_id=0)])
        calls = [mock.call(end_node=3, start_node=1, name="hasMeasure")]
        time_series_service = TimeSeriesService()

        result = time_series_service.save_time_series(time_series_in)

        self.assertEqual(result, time_series_out)
        create_node_mock.assert_has_calls([
            mock.call('`Time Series`'),
            mock.call('`Timestamp`'),
            mock.call('`Timestamp`'),
            mock.call('`Signal Value`'),
            mock.call('`Timestamp`'),
            mock.call('`Timestamp`'),
            mock.call('`Signal Value`')
        ])
        create_properties_mock.assert_has_calls([
            mock.call(time_series_id, time_series_in)
        ])
        create_relationships_mock.assert_has_calls([mock.call(start_node=23, end_node=34, name='takes'),
                                                    mock.call(start_node=34, end_node=34, name='next'),
                                                    mock.call(start_node=1, end_node=35, name='hasSignal'),
                                                    mock.call(start_node=34, end_node=35, name='startInSec'),
                                                    mock.call(start_node=34, end_node=35, name='endInSec'),
                                                    mock.call(start_node=34, end_node=34, name='next'),
                                                    mock.call(start_node=34, end_node=34, name='next'),
                                                    mock.call(start_node=35, end_node=35, name='next'),
                                                    mock.call(start_node=34, end_node=35, name='startInSec'),
                                                    mock.call(start_node=34, end_node=35, name='endInSec')])

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_time_series_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        time_series = TimeSeriesIn(type="Epoch", source="cos", observable_information_id=1, measure_id=2)
        time_series_service = TimeSeriesService()

        result = time_series_service.save_time_series(time_series)

        self.assertEqual(result, TimeSeriesOut(type="Epoch", source="cos", errors=['error']))
        create_node_mock.assert_called_once_with('`Time Series`')
