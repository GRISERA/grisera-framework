import asyncio
import unittest
import unittest.mock as mock

from property.property_model import PropertyIn
from time_series.time_series_router import *
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class TestTimeSeriesRouterPostTransformation(unittest.TestCase):
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

    @mock.patch.object(TimeSeriesServiceGraphDB, 'transform_time_series')
    def test_transform_time_series_without_error(self, transform_time_series_mock):
        dataset_name = "neo4j"
        transform_time_series_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos")
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.transform_time_series(self.transformation, response, dataset_name))

        self.assertEqual(result, TimeSeriesOut(id=1, type="Epoch", source="cos", links=get_links(router)))
        transform_time_series_mock.assert_called_once_with(self.transformation, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'transform_time_series')
    def test_transform_time_series_with_error(self, transform_time_series_mock):
        dataset_name = "neo4j"
        transform_time_series_mock.return_value = TimeSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']})
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.transform_time_series(self.transformation, response, dataset_name))

        self.assertEqual(result, TimeSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']},
                                               links=get_links(router)))
        transform_time_series_mock.assert_called_once_with(self.transformation, dataset_name)
        self.assertEqual(response.status_code, 422)
