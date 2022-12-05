import asyncio
import unittest
import unittest.mock as mock

from measure.measure_router import *
from measure.measure_service_graphdb import MeasureServiceGraphDB


class TestMeasureRouterPut(unittest.TestCase):

    @mock.patch.object(MeasureServiceGraphDB, 'update_measure')
    def test_update_measure_without_error(self, update_measure_mock):
        measure_id = 1
        update_measure_mock.return_value = MeasureOut(datatype="Test", range="Unknown", unit="cm", id=measure_id)
        response = Response()
        measure = MeasurePropertyIn(datatype="Test", range="Unknown", unit="cm")
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.update_measure(
            measure_id, measure, response))

        self.assertEqual(result, MeasureOut(datatype="Test", range="Unknown", unit="cm", id=measure_id, links=get_links(router)))
        update_measure_mock.assert_called_once_with(measure_id, measure)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureServiceGraphDB, 'update_measure')
    def test_update_measure_with_error(self, update_measure_mock):
        measure_id = 1
        update_measure_mock.return_value = MeasureOut(datatype="Test", range="Unknown", unit="cm", errors={'errors': ['test']})
        response = Response()
        measure = MeasurePropertyIn(datatype="Test", unit="cm", range="Unknown")
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.update_measure(
            measure_id, measure, response))

        self.assertEqual(result, MeasureOut(datatype="Test", range="Unknown", unit="cm", errors={'errors': ['test']},
                                            links=get_links(router)))
        update_measure_mock.assert_called_once_with(measure_id, measure)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(MeasureServiceGraphDB, 'update_measure_relationships')
    def test_update_measure_relationships_without_error(self, update_measure_relationships_mock):
        id_node = 1
        update_measure_relationships_mock.return_value = MeasureOut(datatype="Test", unit="cm",
                                                                    range="Unknown", id=id_node)
        response = Response()
        measure_in = MeasureRelationIn(measure_name_id=1)
        measure_out = MeasureOut(datatype="Test", range="Unknown", unit="cm", id=id_node, links=get_links(router))
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.
                             update_measure_relationships(id_node, measure_in, response))

        self.assertEqual(result, measure_out)
        update_measure_relationships_mock.assert_called_once_with(id_node, measure_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureServiceGraphDB, 'update_measure_relationships')
    def test_update_measure_relationships_with_error(self, update_measure_relationships_mock):
        id_node = 1
        update_measure_relationships_mock.return_value = MeasureOut(datatype="Test", unit="cm", range="Unknown", id=id_node,
                                                                    errors="error")
        response = Response()
        measure_in = MeasureRelationIn(measure_name_id=1)
        measure_out = MeasureOut(datatype="Test", range="Unknown", unit="cm", id=id_node, errors="error", links=get_links(router))
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.
                             update_measure_relationships(id_node, measure_in, response))

        self.assertEqual(result, measure_out)
        update_measure_relationships_mock.assert_called_once_with(id_node, measure_in)
        self.assertEqual(response.status_code, 404)
