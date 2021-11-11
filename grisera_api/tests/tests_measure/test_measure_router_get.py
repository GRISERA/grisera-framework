import asyncio
import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut, MeasureOut
from measure.measure_router import *


class TestMeasureRouterGet(unittest.TestCase):

    @mock.patch.object(MeasureService, 'get_measure')
    def test_get_measure_without_error(self, get_measure_mock):
        measure_id = 1
        get_measure_mock.return_value = MeasureOut(data_type="Test", range="Unknown")
        response = Response()
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.get_measure(measure_id, response))

        self.assertEqual(result, MeasureOut(data_type="Test", range="Unknown", links=get_links(router)))
        get_measure_mock.assert_called_once_with(measure_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureService, 'get_measure')
    def test_get_measure_with_error(self, get_measure_mock):
        get_measure_mock.return_value = MeasureOut(data_type="Test", range="Unknown",
                                                   errors={'errors': ['test']})
        response = Response()
        measure_id = 1
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.get_measure(measure_id, response))

        self.assertEqual(result, MeasureOut(data_type="Test", range="Unknown", errors={'errors': ['test']},
                                            links=get_links(router)))
        get_measure_mock.assert_called_once_with(measure_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(MeasureService, 'get_measures')
    def test_get_measures_without_error(self, get_measures_mock):
        get_measures_mock.return_value = MeasuresOut(measures=[
            BasicMeasureOut(data_type="Test", range="Unknown"),
            BasicMeasureOut(data_type="Test", range="Unknown")])
        response = Response()
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.get_measures(response))

        self.assertEqual(result, MeasuresOut(measures=[
            BasicMeasureOut(data_type="Test", range="Unknown"),
            BasicMeasureOut(data_type="Test", range="Unknown")],
            links=get_links(router)))
        get_measures_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
