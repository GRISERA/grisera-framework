import asyncio
import unittest
import unittest.mock as mock

from property.property_model import PropertyIn
from time_series.time_series_router import *
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class TestTimeSeriesRouterPostTransformation(unittest.TestCase):
    transformation = SignalSeriesTransformationIn(
        name="quadrants",
        source_signal_series_ids=[60, 61],
        destination_observable_information_id=102,
        destination_measure_id=103,
        additional_properties=[
            PropertyIn(key="origin_x", value=5),
            PropertyIn(key="origin_y", value=10)
        ]
    )

    @mock.patch.object(TimeSeriesServiceGraphDB, 'transform_signal_series')
    def test_transform_signal_series_without_error(self, transform_signal_series_mock):
        transform_signal_series_mock.return_value = SignalSeriesOut(id=1, type="Epoch", source="cos")
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.transform_signal_series(self.transformation, response))

        self.assertEqual(result, SignalSeriesOut(id=1, type="Epoch", source="cos", links=get_links(router)))
        transform_signal_series_mock.assert_called_once_with(self.transformation)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'transform_signal_series')
    def test_transform_signal_series_with_error(self, transform_signal_series_mock):
        transform_signal_series_mock.return_value = SignalSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']})
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.transform_signal_series(self.transformation, response))

        self.assertEqual(result, SignalSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']},
                                               links=get_links(router)))
        transform_signal_series_mock.assert_called_once_with(self.transformation)
        self.assertEqual(response.status_code, 422)
