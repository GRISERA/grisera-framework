import json
import unittest
import unittest.mock as mock
from modality.modality_service_graphdb import *
from requests import Response


class TestModalityServicePost(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_modality_post_service_without_error(self, mock_requests):
        dataset_name = "neo4j"
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        modality = ModalityIn(modality="motion")
        modality_service = ModalityServiceGraphDB()

        result = modality_service.save_modality(modality, dataset_name)

        self.assertEqual(result, ModalityOut(modality="motion", id=1))

    @mock.patch('graph_api_service.requests')
    def test_modality_post_service_with_error(self, mock_requests):
        dataset_name = "neo4j"
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        modality = ModalityIn(modality="motion")
        modality_service = ModalityServiceGraphDB()

        result = modality_service.save_modality(modality, dataset_name)

        self.assertEqual(result, ModalityOut(modality="motion", errors={'error': 'test'}))
