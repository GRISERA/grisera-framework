import asyncio
import unittest
import unittest.mock as mock
from modality.modality_router import *
from modality.modality_model import BasicModalityOut
from modality.modality_service_graphdb import ModalityServiceGraphDB
from property.property_model import PropertyIn


class TestModalityRouterGet(unittest.TestCase):

    @mock.patch.object(ModalityServiceGraphDB, 'get_modality')
    def test_get_modality_without_error(self, get_modality_mock):
        dataset_name = "neo4j"
        modality_id = 1
        get_modality_mock.return_value = ModalityOut(modality='url', id=modality_id)
        response = Response()
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router.get_modality(modality_id, response, dataset_name))

        self.assertEqual(result, ModalityOut(modality='url', id=modality_id, links=get_links(router)))
        get_modality_mock.assert_called_once_with(modality_id, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ModalityServiceGraphDB, 'get_modality')
    def test_get_modality_with_error(self, get_modality_mock):
        dataset_name = "neo4j"
        get_modality_mock.return_value = ModalityOut(modality='url', errors={'errors': ['test']})
        response = Response()
        modality_id = 1
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router.get_modality(modality_id, response, dataset_name))

        self.assertEqual(result, ModalityOut(modality='url', errors={'errors': ['test']},  links=get_links(router)))
        get_modality_mock.assert_called_once_with(modality_id, dataset_name)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ModalityServiceGraphDB, 'get_modalities')
    def test_get_modality_nodes_without_error(self, get_modalities_mock):
        dataset_name = "neo4j"
        get_modalities_mock.return_value = ModalitiesOut(modalities=[
            BasicModalityOut(modality='url', id=1), BasicModalityOut(modality='url2', id=2)])
        response = Response()
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router.get_modalities(response, dataset_name))

        self.assertEqual(result, ModalitiesOut(modalities=[
            BasicModalityOut(modality='url', id=1), BasicModalityOut(modality='url2', id=2)],
            links=get_links(router)))
        get_modalities_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
