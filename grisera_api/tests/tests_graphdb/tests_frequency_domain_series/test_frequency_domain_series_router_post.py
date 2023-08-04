import asyncio
import unittest
import unittest.mock as mock

from frequency_domain_series.frequency_domain_series_router import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


def return_frequency_domain_series(*args, **kwargs):
    frequency_domain_series_out = SignalSeriesOut(
        id=1, type="Frequencystamp", source="cos")
    return frequency_domain_series_out


class TestFrequencyDomainSeriesRouterPost(unittest.TestCase):

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'save_signal_series')
    def test_create_frequency_domain_series_without_error(self, save_signal_series_mock):
        save_signal_series_mock.side_effect = return_frequency_domain_series
        response = Response()
        frequency_domain_series = SignalSeriesIn(
            id=1, type="Frequencystamp", source="cos")
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.create_frequency_domain_series(
            frequency_domain_series, response))

        self.assertEqual(result, SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", links=get_links(router)))
        save_signal_series_mock.assert_called_once_with(
            frequency_domain_series)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'save_signal_series')
    def test_create_frequency_domain_series_with_error(self, save_signal_series_mock):
        save_signal_series_mock.return_value = SignalSeriesOut(
            type="Frequencystamp", source="cos", errors={'errors': ['test']})
        response = Response()
        frequency_domain_series = SignalSeriesIn(
            id=1, type="Frequencystamp", source="cos")
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.create_frequency_domain_series(
            frequency_domain_series, response))

        self.assertEqual(result, SignalSeriesOut(type="Frequencystamp", source="cos", errors={'errors': ['test']},
                                                 links=get_links(router)))
        save_signal_series_mock.assert_called_once_with(
            frequency_domain_series)
        self.assertEqual(response.status_code, 422)
