import asyncio
import unittest
import unittest.mock as mock

from measure.measure_router import *


class TestMeasureRouterPost(unittest.TestCase):

    @mock.patch.object(MeasureService, 'save_measure')
    def test_create_measure_without_error(self, save_measure_mock):
        save_measure_mock.return_value = MeasureOut(data_type="Test", range="Unknown", id=1)
        response = Response()
        measure = MeasureIn(measure_name_id=1, data_type="Test", range="Unknown")
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.create_measure(measure, response))

        self.assertEqual(result, MeasureOut(data_type="Test",
                                            range="Unknown", id=1, links=get_links(router)))
        save_measure_mock.assert_called_once_with(measure)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureService, 'save_measure')
    def test_create_measure_with_error(self, save_measure_mock):
        save_measure_mock.return_value = MeasureOut(data_type="Test",
                                                    range="Unknown", errors={'errors': ['test']})
        response = Response()
        measure = MeasureIn(measure_name_id=1, data_type="Test", range="Unknown")
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.create_measure(measure, response))

        self.assertEqual(result, MeasureOut(data_type="Test", range="Unknown",
                                            errors={'errors': ['test']}, links=get_links(router)))
        save_measure_mock.assert_called_once_with(measure)
        self.assertEqual(response.status_code, 422)
