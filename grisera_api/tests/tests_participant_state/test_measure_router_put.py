import asyncio
import unittest
import unittest.mock as mock
from measure.measure_router import *


class TestMeasureRouterPut(unittest.TestCase):

    @mock.patch.object(MeasureService, 'update_measure')
    def test_update_measure_without_error(self, update_measure_mock):
        measure_id = 1
        update_measure_mock.return_value = MeasureOut(data_type="Test", range="Unknown", id=measure_id)
        response = Response()
        measure = MeasurePropertyIn(data_type="Test", range="Unknown",)
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.update_measure(
            measure_id, measure, response))

        self.assertEqual(result, MeasureOut(data_type="Test", range="Unknown", id=measure_id, links=get_links(router)))
        update_measure_mock.assert_called_once_with(measure_id, measure)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureService, 'update_measure')
    def test_update_measure_with_error(self, update_measure_mock):
        measure_id = 1
        update_measure_mock.return_value = MeasureOut(data_type="Test", range="Unknown", errors={'errors': ['test']})
        response = Response()
        measure = MeasurePropertyIn(data_type="Test", range="Unknown",)
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.update_measure(
            measure_id, measure, response))

        self.assertEqual(result, MeasureOut(data_type="Test", range="Unknown", errors={'errors': ['test']},
                                                             links=get_links(router)))
        update_measure_mock.assert_called_once_with(measure_id, measure)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(MeasureService, 'update_measure_relationships')
    def test_update_measure_relationships_without_error(self, update_measure_relationships_mock):
        id_node = 1
        update_measure_relationships_mock.return_value = MeasureOut(data_type="Test", range="Unknown", id=id_node)
        response = Response()
        measure_in = MeasureRelationIn(measure_name_id=2)
        measure_out = MeasureOut(data_type="Test", range="Unknown", id=id_node, links=get_links(router))
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.
                             update_measure_relationships(id_node, measure_in, response))

        self.assertEqual(result, measure_out)
        update_measure_relationships_mock.assert_called_once_with(id_node, measure_in)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureService, 'update_measure_relationships')
    def test_update_measure_relationships_with_error(self, update_measure_relationships_mock):
        id_node = 1
        update_measure_relationships_mock.return_value = MeasureOut(data_type="Test", range="Unknown", id=id_node, errors="error")
        response = Response()
        measure_in = MeasureRelationIn(measure_name_id=4)
        measure_out = MeasureOut(data_type="Test", range="Unknown", id=id_node, errors="error", links=get_links(router))
        measure_router = MeasureRouter()

        result = asyncio.run(measure_router.
                             update_measure_relationships(id_node, measure_in, response))

        self.assertEqual(result, measure_out)
        update_measure_relationships_mock.assert_called_once_with(id_node, measure_in)
        self.assertEqual(response.status_code, 404)
