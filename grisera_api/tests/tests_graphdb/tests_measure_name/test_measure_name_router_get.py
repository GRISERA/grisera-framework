import asyncio
import unittest
import unittest.mock as mock
from measure_name.measure_name_router import *
from measure_name.measure_name_model import BasicMeasureNameOut
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB


class TestMeasureNameRouterGet(unittest.TestCase):

    @mock.patch.object(MeasureNameServiceGraphDB, 'get_measure_name')
    def test_get_measure_name_without_error(self, get_measure_name_mock):
        dataset_name = "neo4j"
        measure_name_id = 1
        get_measure_name_mock.return_value = MeasureNameOut(name="Familiarity", type="Additional emotions measure",
                                                            id=measure_name_id)
        response = Response()
        measure_name_router = MeasureNameRouter()

        result = asyncio.run(measure_name_router.get_measure_name(measure_name_id, response, dataset_name))


        self.assertEqual(result, MeasureNameOut(name="Familiarity", type="Additional emotions measure",
                                                id=measure_name_id, links=get_links(router)))
        get_measure_name_mock.assert_called_once_with(measure_name_id,dataset_name, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(MeasureNameServiceGraphDB, 'get_measure_name')
    def test_get_measure_name_with_error(self, get_measure_name_mock):
        dataset_name = "neo4j"
        get_measure_name_mock.return_value = MeasureNameOut(name="Familiarity", type="Additional emotions measure", errors={'errors': ['test']})
        response = Response()
        measure_name_id = 1
        measure_name_router = MeasureNameRouter()

        result = asyncio.run(measure_name_router.get_measure_name(measure_name_id, response, dataset_name))


        self.assertEqual(result, MeasureNameOut(name="Familiarity", type="Additional emotions measure",
                                                errors={'errors': ['test']},  links=get_links(router)))
        get_measure_name_mock.assert_called_once_with(measure_name_id,dataset_name, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(MeasureNameServiceGraphDB, 'get_measure_names')
    def test_get_measure_name_nodes_without_error(self, get_measure_names_mock):
        dataset_name = "neo4j"
        get_measure_names_mock.return_value = MeasureNamesOut(measure_names=[
            BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=1),
            BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=2)])
        response = Response()
        measure_name_router = MeasureNameRouter()

        result = asyncio.run(measure_name_router.get_measure_names(response, dataset_name))

        self.assertEqual(result, MeasureNamesOut(measure_names=[
            BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=1),
            BasicMeasureNameOut(name="Familiarity", type="Additional emotions measure", id=2)],
            links=get_links(router)))
        get_measure_names_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
