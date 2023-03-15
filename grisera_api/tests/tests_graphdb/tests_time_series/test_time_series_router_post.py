import asyncio
import unittest
import unittest.mock as mock

from grisera_api.time_series.time_series_router import *
from grisera_api.time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


def return_time_series(*args, **kwargs):
    time_series_out = TimeSeriesOut(id=1, type="Epoch", source="cos")
    return time_series_out


class TestTimeSeriesRouterPost(unittest.TestCase):

    @mock.patch.object(TimeSeriesServiceGraphDB, 'save_time_series')
    def test_create_time_series_without_error(self, save_time_series_mock):
        save_time_series_mock.side_effect = return_time_series
        response = Response()
        time_series = TimeSeriesIn(id=1, type="Epoch", source="cos")
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.create_time_series(time_series, response))

        self.assertEqual(result, TimeSeriesOut(id=1, type="Epoch", source="cos", links=get_links(router)))
        save_time_series_mock.assert_called_once_with(time_series)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'save_time_series')
    def test_create_time_series_with_error(self, save_time_series_mock):
        save_time_series_mock.return_value = TimeSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']})
        response = Response()
        time_series = TimeSeriesIn(id=1, type="Epoch", source="cos")
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.create_time_series(time_series, response))

        self.assertEqual(result, TimeSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']},
                                               links=get_links(router)))
        save_time_series_mock.assert_called_once_with(time_series)
        self.assertEqual(response.status_code, 422)
