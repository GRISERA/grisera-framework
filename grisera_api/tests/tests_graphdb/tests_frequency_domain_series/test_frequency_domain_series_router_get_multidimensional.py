import asyncio
import unittest
import unittest.mock as mock

from frequency_domain_series.frequency_domain_series_router import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


class TestFrequencyDomainSeriesRouterPostTransformation(unittest.TestCase):

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'get_signal_series_multidimensional')
    def test_get_signal_series_multidimensional_without_error(self, get_signal_series_multidimensional_mock):
        get_signal_series_multidimensional_mock.return_value = SignalSeriesMultidimensionalOut(
            signal_values=[])
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(
            frequency_domain_series_router.get_signal_series_multidimensional("15, 20, 25", response))

        self.assertEqual(SignalSeriesMultidimensionalOut(
            signal_values=[], links=get_links(router)), result)
        get_signal_series_multidimensional_mock.assert_called_once_with([
                                                                        15, 20, 25])
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'get_signal_series_multidimensional')
    def test_get_signal_series_multidimensional_with_error(self, get_signal_series_multidimensional_mock):
        get_signal_series_multidimensional_mock.return_value = SignalSeriesMultidimensionalOut(
            errors={'errors': ['test']})
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(
            frequency_domain_series_router.get_signal_series_multidimensional("15, 20, 25", response))

        self.assertEqual(SignalSeriesMultidimensionalOut(errors={'errors': ['test']},
                                                         links=get_links(router)), result)
        get_signal_series_multidimensional_mock.assert_called_once_with([
                                                                        15, 20, 25])
        self.assertEqual(response.status_code, 404)
