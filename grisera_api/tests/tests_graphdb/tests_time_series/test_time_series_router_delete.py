import asyncio
import unittest
import unittest.mock as mock
from time_series.time_series_router import *
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class TestTimeSeriesRouterDelete(unittest.TestCase):

    @mock.patch.object(TimeSeriesServiceGraphDB, 'delete_time_series')
    def test_delete_time_series_without_error(self, delete_time_series_mock):
        dataset_name = "neo4j"
        time_series_id = 1
        delete_time_series_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos")
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.delete_time_series(time_series_id, response, dataset_name))

        self.assertEqual(result, TimeSeriesOut(id=1, type="Epoch", source="cos", links=get_links(router)))
        delete_time_series_mock.assert_called_once_with(time_series_id, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'delete_time_series')
    def test_delete_time_series_with_error(self, delete_time_series_mock):
        dataset_name = "neo4j"
        delete_time_series_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos", errors={'errors': ['test']})
        response = Response()
        time_series_id = 1
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.delete_time_series(time_series_id, response, dataset_name))

        self.assertEqual(result, TimeSeriesOut(id=1, type="Epoch", source="cos",
                                               errors={'errors': ['test']}, links=get_links(router)))
        delete_time_series_mock.assert_called_once_with(time_series_id, dataset_name)
        self.assertEqual(response.status_code, 404)
