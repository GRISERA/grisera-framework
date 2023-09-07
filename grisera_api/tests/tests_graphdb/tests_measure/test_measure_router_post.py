import asyncio
import unittest
import unittest.mock as mock

from measure.measure_router import *
from measure.measure_service_graphdb import MeasureServiceGraphDB


class TestMeasureRouterPost(unittest.TestCase):

    @mock.patch.object(MeasureServiceGraphDB, 'save_measure')
    def test_create_measure_without_error(self, save_measure_mock):
        dataset_name = "neo4j"
        save_measure_mock.return_value = MeasureOut(datatype="Test", range="Unknown", unit="cm", id=1)
        response = Response()
        measure = MeasureIn(measure_name_id=1, datatype="Test", range="Unknown", unit="cm")
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.create_measure(measure, response, dataset_name))

        self.assertEqual(result, MeasureOut(datatype="Test",
                                            range="Unknown", id=1, unit="cm", links=get_links(router)))
        save_measure_mock.assert_called_once_with(measure, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureServiceGraphDB, 'save_measure')
    def test_create_measure_with_error(self, save_measure_mock):
        dataset_name = "neo4j"
        save_measure_mock.return_value = MeasureOut(datatype="Test",
                                                    range="Unknown", unit="cm", errors={'errors': ['test']})
        response = Response()
        measure = MeasureIn(measure_name_id=1, datatype="Test", unit="cm", range="Unknown")
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.create_measure(measure, response, dataset_name))

        self.assertEqual(result, MeasureOut(datatype="Test", unit="cm", range="Unknown",
                                            errors={'errors': ['test']}, links=get_links(router)))
        save_measure_mock.assert_called_once_with(measure, dataset_name)
        self.assertEqual(response.status_code, 422)
