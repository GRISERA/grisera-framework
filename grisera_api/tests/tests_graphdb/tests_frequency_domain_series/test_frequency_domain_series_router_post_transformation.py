import asyncio
import unittest
import unittest.mock as mock

from property.property_model import PropertyIn
from frequency_domain_series.frequency_domain_series_router import *
from frequency_domain_series.frequency_domain_series_service_graphdb import FrequencyDomainSeriesServiceGraphDB


class TestFrequencyDomainSeriesRouterPostTransformation(unittest.TestCase):
    transformation = SignalSeriesTransformationIn(
        name="quadrants",
        source_signal_series_ids=[60, 61],
        destination_observable_information_id=102,
        destination_measure_id=103,
        additional_properties=[
            PropertyIn(key="origin_x", value=5),
            PropertyIn(key="origin_y", value=10)
        ]
    )

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'transform_signal_series')
    def test_transform_signal_series_without_error(self, transform_signal_series_mock):
        transform_signal_series_mock.return_value = SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos")
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.transform_signal_series(
            self.transformation, response))

        self.assertEqual(result, SignalSeriesOut(
            id=1, type="Frequencystamp", source="cos", links=get_links(router)))
        transform_signal_series_mock.assert_called_once_with(
            self.transformation)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(FrequencyDomainSeriesServiceGraphDB, 'transform_signal_series')
    def test_transform_signal_series_with_error(self, transform_signal_series_mock):
        transform_signal_series_mock.return_value = SignalSeriesOut(
            type="Frequencystamp", source="cos", errors={'errors': ['test']})
        response = Response()
        frequency_domain_series_router = FrequencyDomainSeriesRouter()

        result = asyncio.run(frequency_domain_series_router.transform_signal_series(
            self.transformation, response))

        self.assertEqual(result, SignalSeriesOut(type="Frequencystamp", source="cos", errors={'errors': ['test']},
                                                 links=get_links(router)))
        transform_signal_series_mock.assert_called_once_with(
            self.transformation)
        self.assertEqual(response.status_code, 422)
