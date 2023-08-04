import asyncio
import unittest
import unittest.mock as mock
from typing import Dict

from pydantic import BaseModel

from signal_series.signal_series_model import SignalSeriesOut, SignalSeriesNodesOut
from frequency_domain_series.frequency_domain_series_router import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


class TestRequest(BaseModel):
    """
    Model of test request
    Attributes:
        query_params (Optional[Dict[str, str]]): Query params
    """
    query_params: Optional[Dict[str, str]]


class TestFrequencyDomainSeriesRouterGet(unittest.TestCase):

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'get_signal_series')
    def test_get_signal_series_without_error(self, get_signal_series_mock):
        frequency_domain_series_id = 1
        get_signal_series_mock.return_value = SignalSeriesOut(
            type="Frequencystamp", source="cos")
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.get_signal_series(
            frequency_domain_series_id, 0, response, 10, 20))

        self.assertEqual(result, SignalSeriesOut(
            type="Frequencystamp", source="cos", links=get_links(router)))
        get_signal_series_mock.assert_called_once_with(
            frequency_domain_series_id, 0, 10, 20)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'get_signal_series')
    def test_get_signal_series_with_error(self, get_signal_series_mock):
        get_signal_series_mock.return_value = SignalSeriesOut(
            type="Frequencystamp", source="cos", errors={'errors': ['test']})
        response = Response()
        frequency_domain_series_id = 1
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.get_signal_series(
            frequency_domain_series_id, 0, response, 10, 20))

        self.assertEqual(result, SignalSeriesOut(type="Frequencystamp", source="cos", errors={'errors': ['test']},
                                                 links=get_links(router)))
        get_signal_series_mock.assert_called_once_with(
            frequency_domain_series_id, 0, 10, 20)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'get_signal_series_nodes')
    def test_get_signal_series_nodes_without_error(self, get_signal_series_nodes_mock):
        get_signal_series_nodes_mock.return_value = SignalSeriesNodesOut(signal_series_nodes=[
            SignalSeriesOut(type="Frequencystamp", source="cos"),
            SignalSeriesOut(type="Frequencystamp", source="test")])
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(
            frequency_domain_series_router.get_signal_series_nodes(response, TestRequest(query_params={"abc": "def"})))

        self.assertEqual(result, SignalSeriesNodesOut(signal_series_nodes=[
            SignalSeriesOut(type="Frequencystamp", source="cos"),
            SignalSeriesOut(type="Frequencystamp", source="test")],
            links=get_links(router)))
        get_signal_series_nodes_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
