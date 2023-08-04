import asyncio
import unittest
import unittest.mock as mock
from frequency_domain_series.frequency_domain_series_router import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


class TestFrequencyDomainSeriesRouterDelete(unittest.TestCase):

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'delete_signal_series')
    def test_delete_signal_series_without_error(self, delete_signal_series_mock):
        frequency_domain_series_id = 1
        delete_signal_series_mock.return_value = SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos")
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.delete_signal_series(
            frequency_domain_series_id, response))

        self.assertEqual(result, SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", links=get_links(router)))
        delete_signal_series_mock.assert_called_once_with(
            frequency_domain_series_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'delete_signal_series')
    def test_delete_signal_series_with_error(self, delete_signal_series_mock):
        delete_signal_series_mock.return_value = SignalSeriesOut(id=1, type="Frequencystamp", source="cos",
                                                                 errors={'errors': ['test']})
        response = Response()
        frequency_domain_series_id = 1
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.delete_signal_series(
            frequency_domain_series_id, response))

        self.assertEqual(result, SignalSeriesOut(id=1, type="Frequencystamp", source="cos",
                                                 errors={'errors': ['test']}, links=get_links(router)))
        delete_signal_series_mock.assert_called_once_with(
            frequency_domain_series_id)
        self.assertEqual(response.status_code, 404)
