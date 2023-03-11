import asyncio
import unittest
import unittest.mock as mock

from measure.measure_model import BasicMeasureOut, MeasureOut
from measure.measure_router import *
from measure.measure_service_graphdb import MeasureServiceGraphDB


class TestMeasureRouterGet(unittest.TestCase):

    @mock.patch.object(MeasureServiceGraphDB, 'get_measure')
    def test_get_measure_without_error(self, get_measure_mock):
        database_name = "neo4j"
        measure_id = 1
        get_measure_mock.return_value = MeasureOut(datatype="Test", range="Unknown", unit="cm", )
        response = Response()
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.get_measure(measure_id, response, database_name))

        self.assertEqual(result, MeasureOut(datatype="Test", range="Unknown", unit="cm", links=get_links(router)))
        get_measure_mock.assert_called_once_with(measure_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureServiceGraphDB, 'get_measure')
    def test_get_measure_with_error(self, get_measure_mock):
        database_name = "neo4j"
        get_measure_mock.return_value = MeasureOut(datatype="Test", range="Unknown", unit="cm",
                                                   errors={'errors': ['test']})
        response = Response()
        measure_id = 1
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.get_measure(measure_id, response, database_name))

        self.assertEqual(result, MeasureOut(datatype="Test", range="Unknown", unit="cm", errors={'errors': ['test']},
                                            links=get_links(router)))
        get_measure_mock.assert_called_once_with(measure_id, database_name)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(MeasureServiceGraphDB, 'get_measures')
    def test_get_measures_without_error(self, get_measures_mock):
        database_name = "neo4j"
        get_measures_mock.return_value = MeasuresOut(measures=[
            BasicMeasureOut(datatype="Test", range="Unknown", unit="cm"),
            BasicMeasureOut(datatype="Test", range="Unknown", unit="cm")])
        response = Response()
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.get_measures(response, database_name))

        self.assertEqual(result, MeasuresOut(measures=[
            BasicMeasureOut(datatype="Test", range="Unknown", unit="cm"),
            BasicMeasureOut(datatype="Test", range="Unknown", unit="cm")],
            links=get_links(router)))
        get_measures_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
