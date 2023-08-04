import asyncio
import unittest
import unittest.mock as mock
from frequency_domain_series.frequency_domain_series_router import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


class TestFrequencyDomainSeriesRouterPut(unittest.TestCase):

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'update_signal_series')
    def test_update_signal_series_without_error(self, update_signal_series_mock):
        frequency_domain_series_id = 1
        update_signal_series_mock.return_value = SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos")
        response = Response()
        frequency_domain_series = SignalSeriesPropertyIn(
            id=1, type="Frequencystamp", source="cos")
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.update_signal_series(
            frequency_domain_series_id, frequency_domain_series, response))

        self.assertEqual(result, SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", links=get_links(router)))
        update_signal_series_mock.assert_called_once_with(
            frequency_domain_series_id, frequency_domain_series)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'update_signal_series')
    def test_update_signal_series_with_error(self, update_signal_series_mock):
        frequency_domain_series_id = 1
        update_signal_series_mock.return_value = SignalSeriesOut(id=1, type="Frequencystamp", source="cos",
                                                                 errors={'errors': ['test']})
        response = Response()
        frequency_domain_series = SignalSeriesPropertyIn(
            id=1, type="Frequencystamp", source="cos")
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.update_signal_series(
            frequency_domain_series_id, frequency_domain_series, response))

        self.assertEqual(result, SignalSeriesOut(id=1, type="Frequencystamp", source="cos", errors={'errors': ['test']},
                                                 links=get_links(router)))
        update_signal_series_mock.assert_called_once_with(
            frequency_domain_series_id, frequency_domain_series)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'update_signal_series_relationships')
    def test_update_signal_series_relationships_without_error(self, update_signal_series_relationships_mock):
        id_node = 1
        update_signal_series_relationships_mock.return_value = SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos")
        response = Response()
        frequency_domain_series_in = SignalSeriesRelationIn(
            observable_information_id=2, measure_id=3)
        frequency_domain_series_out = SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", links=get_links(router))
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.
                             update_signal_series_relationships(id_node, frequency_domain_series_in, response))

        self.assertEqual(result, frequency_domain_series_out)
        update_signal_series_relationships_mock.assert_called_once_with(
            id_node, frequency_domain_series_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'update_signal_series_relationships')
    def test_update_signal_series_relationships_with_error(self, update_signal_series_relationships_mock):
        id_node = 1
        update_signal_series_relationships_mock.return_value = SignalSeriesOut(id=1, type="Frequencystamp", source="cos",
                                                                               errors="error")
        response = Response()
        frequency_domain_series_in = SignalSeriesRelationIn(
            observable_information_id=2, measure_id=3)
        frequency_domain_series_out = SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", errors="error", links=get_links(router))
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.
                             update_signal_series_relationships(id_node, frequency_domain_series_in, response))

        self.assertEqual(result, frequency_domain_series_out)
        update_signal_series_relationships_mock.assert_called_once_with(
            id_node, frequency_domain_series_in)
        self.assertEqual(response.status_code, 404)
