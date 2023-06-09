import asyncio
import unittest
import unittest.mock as mock

from time_series.time_series_router import *
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class TestTimeSeriesRouterPostTransformation(unittest.TestCase):

    @mock.patch.object(TimeSeriesServiceGraphDB, 'get_time_series_multidimensional')
    def test_get_time_series_multidimensional_without_error(self, get_time_series_multidimensional_mock):
        get_time_series_multidimensional_mock.return_value = SignalSeriesMultidimensionalOut(signal_values=[])
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.get_time_series_multidimensional("15, 20, 25", response))

        self.assertEqual(SignalSeriesMultidimensionalOut(signal_values=[], links=get_links(router)), result)
        get_time_series_multidimensional_mock.assert_called_once_with([15, 20, 25])
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'get_time_series_multidimensional')
    def test_get_time_series_multidimensional_with_error(self, get_time_series_multidimensional_mock):
        get_time_series_multidimensional_mock.return_value = SignalSeriesMultidimensionalOut(errors={'errors': ['test']})
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.get_time_series_multidimensional("15, 20, 25", response))

        self.assertEqual(SignalSeriesMultidimensionalOut(errors={'errors': ['test']},
                                                       links=get_links(router)), result)
        get_time_series_multidimensional_mock.assert_called_once_with([15, 20, 25])
        self.assertEqual(response.status_code, 404)
