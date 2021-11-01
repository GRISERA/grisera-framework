import asyncio
import unittest
import unittest.mock as mock

from measure.measure_router import *


class TestMeasureRouterDelete(unittest.TestCase):

    @mock.patch.object(MeasureService, 'delete_measure')
    def test_delete_measure_without_error(self, delete_measure_mock):
        measure_id = 1
        delete_measure_mock.return_value = MeasureOut(measure_name="ECG", data_type="Test", range="Unknown",
                                                      id=measure_id)
        response = Response()
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.delete_measure(measure_id, response))

        self.assertEqual(result, MeasureOut(measure_name="ECG", data_type="Test", range="Unknown", id=measure_id,
                                            links=get_links(router)))
        delete_measure_mock.assert_called_once_with(measure_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureService, 'delete_measure')
    def test_delete_measure_with_error(self, delete_measure_mock):
        delete_measure_mock.return_value = MeasureOut(measure_name="ECG", data_type="Test", range="Unknown",
                                                      errors={'errors': ['test']})
        response = Response()
        measure_id = 1
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.delete_measure(measure_id, response))

        self.assertEqual(result,
                         MeasureOut(measure_name="ECG", data_type="Test", range="Unknown", errors={'errors': ['test']},
                                    links=get_links(router)))
        delete_measure_mock.assert_called_once_with(measure_id)
        self.assertEqual(response.status_code, 404)
