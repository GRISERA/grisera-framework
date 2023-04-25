import asyncio
import unittest
import unittest.mock as mock
from time_series.time_series_router import *
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class TestTimeSeriesRouterPut(unittest.TestCase):

    @mock.patch.object(TimeSeriesServiceGraphDB, 'update_time_series')
    def test_update_time_series_without_error(self, update_time_series_mock):
        dataset_name = "neo4j"
        time_series_id = 1
        update_time_series_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos")
        response = Response()
        time_series = TimeSeriesPropertyIn(id=1, type="Epoch", source="cos")
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.update_time_series(
            time_series_id, time_series, response))

        self.assertEqual(result, TimeSeriesOut(id=1, type="Epoch", source="cos", links=get_links(router)))
        update_time_series_mock.assert_called_once_with(time_series_id, time_series)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'update_time_series')
    def test_update_time_series_with_error(self, update_time_series_mock):
        dataset_name = "neo4j"
        time_series_id = 1
        update_time_series_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos", errors={'errors': ['test']})
        response = Response()
        time_series = TimeSeriesPropertyIn(id=1, type="Epoch", source="cos")
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.update_time_series(
            time_series_id, time_series, response))

        self.assertEqual(result, TimeSeriesOut(id=1, type="Epoch", source="cos", errors={'errors': ['test']},
                                               links=get_links(router)))
        update_time_series_mock.assert_called_once_with(time_series_id, time_series)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'update_time_series_relationships')
    def test_update_time_series_relationships_without_error(self, update_time_series_relationships_mock):
        dataset_name = "neo4j"
        id_node = 1
        update_time_series_relationships_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos")
        response = Response()
        time_series_in = TimeSeriesRelationIn(observable_information_id=2, measure_id=3)
        time_series_out = TimeSeriesOut(id=1, type="Epoch", source="cos", links=get_links(router))
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.
                             update_time_series_relationships(id_node, time_series_in, response))

        self.assertEqual(result, time_series_out)
        update_time_series_relationships_mock.assert_called_once_with(id_node, time_series_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'update_time_series_relationships')
    def test_update_time_series_relationships_with_error(self, update_time_series_relationships_mock):
        dataset_name = "neo4j"
        id_node = 1
        update_time_series_relationships_mock.return_value = TimeSeriesOut(id=1, type="Epoch", source="cos",
                                                                           errors="error")
        response = Response()
        time_series_in = TimeSeriesRelationIn(observable_information_id=2, measure_id=3)
        time_series_out = TimeSeriesOut(id=1, type="Epoch", source="cos", errors="error", links=get_links(router))
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.
                             update_time_series_relationships(id_node, time_series_in, response))

        self.assertEqual(result, time_series_out)
        update_time_series_relationships_mock.assert_called_once_with(id_node, time_series_in)
        self.assertEqual(response.status_code, 404)
