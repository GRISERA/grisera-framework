import json
import unittest
import unittest.mock as mock

from measure_name.measure_name_model import *
from measure_name.measure_name_service_graphdb import *
from requests import Response


class TestMeasureNameServicePost(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_measure_name_post_service_without_error(self, mock_requests):
        dataset_name = "neo4j"
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        measure_name = MeasureNameIn(name="Familiarity", type="Addional emotions measure")
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.save_measure_name(measure_name, dataset_name)

        self.assertEqual(result, MeasureNameOut(name="Familiarity", type="Addional emotions measure", id=1))

    @mock.patch('graph_api_service.requests')
    def test_measure_name_post_service_with_error(self, mock_requests):
        dataset_name = "neo4j"
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        measure_name = MeasureNameIn(name="Familiarity", type="Addional emotions measure")
        measure_name_service = MeasureNameServiceGraphDB()

        result = measure_name_service.save_measure_name(measure_name, dataset_name)

        self.assertEqual(result, MeasureNameOut(name="Familiarity", type="Addional emotions measure",
                                                errors={'error': 'test'}))
