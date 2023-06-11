import asyncio
import unittest
import unittest.mock as mock
from typing import Dict

from pydantic import BaseModel

from time_series.time_series_router import *
from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesNodesOut
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class TestRequest(BaseModel):
    """
    Model of test request
    Attributes:
        query_params (Optional[Dict[str, str]]): Query params
    """
    query_params: Optional[Dict[str, str]]


class TestTimeSeriesRouterGet(unittest.TestCase):

    @mock.patch.object(TimeSeriesServiceGraphDB, 'get_signal_series')
    def test_get_signal_series_without_error(self, get_signal_series_mock):
        time_series_id = 1
        get_signal_series_mock.return_value = SignalSeriesOut(type="Epoch", source="cos")
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.get_signal_series(time_series_id, 0, response, 10, 20))

        self.assertEqual(result, SignalSeriesOut(type="Epoch", source="cos", links=get_links(router)))
        get_signal_series_mock.assert_called_once_with(time_series_id, 0, 10, 20)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'get_signal_series')
    def test_get_signal_series_with_error(self, get_signal_series_mock):
        get_signal_series_mock.return_value = SignalSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']})
        response = Response()
        time_series_id = 1
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(time_series_router.get_signal_series(time_series_id, 0, response, 10, 20))

        self.assertEqual(result, SignalSeriesOut(type="Epoch", source="cos", errors={'errors': ['test']},
                                               links=get_links(router)))
        get_signal_series_mock.assert_called_once_with(time_series_id, 0, 10, 20)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(TimeSeriesServiceGraphDB, 'get_signal_series_nodes')
    def test_get_signal_series_nodes_without_error(self, get_signal_series_nodes_mock):
        get_signal_series_nodes_mock.return_value = SignalSeriesNodesOut(time_series_nodes=[
            SignalSeriesOut(type="Epoch", source="cos"),
            SignalSeriesOut(type="Epoch", source="test")])
        response = Response()
        time_series_router = TimeSeriesRouter()

        result = asyncio.run(
            time_series_router.get_signal_series_nodes(response, TestRequest(query_params={"abc": "def"})))

        self.assertEqual(result, SignalSeriesNodesOut(time_series_nodes=[
            SignalSeriesOut(type="Epoch", source="cos"),
            SignalSeriesOut(type="Epoch", source="test")],
            links=get_links(router)))
        get_signal_series_nodes_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
