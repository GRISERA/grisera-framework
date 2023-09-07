import unittest
from unittest import mock

from graph_api_service import GraphApiService
from property.property_model import PropertyIn
from time_series.time_series_model import TimeSeriesOut, TimeSeriesTransformationIn, TimeSeriesIn, Type, \
    TimeSeriesTransformationRelationshipIn
from time_series.time_series_service_graphdb_with_signal_values import TimeSeriesServiceGraphDBWithSignalValues


class TestTimeSeriesWithSignalValuesServiceTransformation(unittest.TestCase):
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'create_relationship_properties')
    def test_transform_time_series_without_errors(self, create_relationship_properties_mock, create_relationships_mock):
        dataset_name = "neo4j"
        transformation = TimeSeriesTransformationIn(
            name="quadrants",
            source_time_series_ids=[60, 61],
            destination_observable_information_id=102,
            destination_measure_id=103,
            additional_properties=[
                PropertyIn(key="origin_x", value=5),
                PropertyIn(key="origin_y", value=10)
            ]
        )
        result_timeseries = TimeSeriesOut(
            id=50,
            type=Type.timestamp,
            observable_information_id=102,
            measure_id=103,
            signal_values=[
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 22,
                                     'properties': [{'key': 'value', 'value': '4'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 21, 'properties': [
                        {'key': 'timestamp', 'value': '100'}]}
                },
                {
                    'signal_value': {'labels': ['Signal Value'], 'id': 24,
                                     'properties': [
                                         {'key': 'value', 'value': '3'}]},
                    'timestamp': {'labels': ['Timestamp'], 'id': 23, 'properties': [
                        {'key': 'timestamp', 'value': '200'}]}
                }
            ],
            additional_properties=[
                PropertyIn(key='origin_x', value='5'),
                PropertyIn(key='origin_y', value='10'),
                PropertyIn(key='transformation_name', value='quadrants')
            ]
        )

        def get_time_series_side_effect(time_series_id: int, dataset_name: str):
            if time_series_id == 60:
                return TimeSeriesOut(
                    id=time_series_id,
                    type=Type.timestamp,
                    signal_values=[
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 2,
                                             'properties': [
                                                 {'key': 'value', 'value': '10'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 1,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '100'}]}
                        },
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 4,
                                             'properties': [
                                                 {'key': 'value', 'value': '-10'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 3,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '200'}]}
                        }
                    ])
            elif time_series_id == 61:
                return TimeSeriesOut(
                    id=time_series_id,
                    type=Type.timestamp,
                    signal_values=[
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 12,
                                             'properties': [
                                                 {'key': 'value', 'value': '-5'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 11,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '100'}]}
                        },
                        {
                            'signal_value': {'labels': ['Signal Value'], 'id': 14,
                                             'properties': [
                                                 {'key': 'value', 'value': '5'}]},
                            'timestamp': {'labels': ['Timestamp'], 'id': 13,
                                          'properties': [
                                              {'key': 'timestamp', 'value': '200'}]}
                        }
                    ])
            else:
                return None

        def save_time_series_side_effect(time_series: TimeSeriesIn, dataset_name: str):
            return result_timeseries

        def create_relationships_side_effect(id_from: int, id_to: int, name: str, dataset_name: str):
            return {"id": 100 * id_from + id_to}

        create_relationships_mock.side_effect = create_relationships_side_effect

        time_series_service = TimeSeriesServiceGraphDBWithSignalValues()
        time_series_service.get_time_series = get_time_series_side_effect
        time_series_service.save_time_series = save_time_series_side_effect
        result = time_series_service.transform_time_series(transformation, dataset_name)

        self.assertEqual(result_timeseries, result)
        self.assertEqual([
            mock.call(50, 60, 'transformedFrom', dataset_name),
            mock.call(50, 61, 'transformedFrom', dataset_name),
            mock.call(22, 2, 'basedOn', dataset_name),
            mock.call(22, 12, 'basedOn', dataset_name),
            mock.call(24, 4, 'basedOn', dataset_name),
            mock.call(24, 14, 'basedOn', dataset_name)
        ], create_relationships_mock.call_args_list)
        self.assertEqual([
            mock.call(5060, TimeSeriesTransformationRelationshipIn(
                additional_properties=[PropertyIn(key='order', value='1')]), dataset_name),
            mock.call(5061, TimeSeriesTransformationRelationshipIn(
                additional_properties=[PropertyIn(key='order', value='2')]), dataset_name),
            mock.call(2202, TimeSeriesTransformationRelationshipIn(
                additional_properties=[PropertyIn(key='order', value='1')]), dataset_name),
            mock.call(2212, TimeSeriesTransformationRelationshipIn(
                additional_properties=[PropertyIn(key='order', value='2')]), dataset_name),
            mock.call(2404, TimeSeriesTransformationRelationshipIn(
                additional_properties=[PropertyIn(key='order', value='1')]), dataset_name),
            mock.call(2414, TimeSeriesTransformationRelationshipIn(
                additional_properties=[PropertyIn(key='order', value='2')]), dataset_name)
        ], create_relationship_properties_mock.call_args_list)
