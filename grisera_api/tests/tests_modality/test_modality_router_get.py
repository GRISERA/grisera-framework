import asyncio
import unittest
import unittest.mock as mock
from modality.modality_router import *
from modality.modality_model import BasicModalityOut
from property.property_model import PropertyIn


class TestModalityRouterGet(unittest.TestCase):

    @mock.patch.object(ModalityService, 'get_modality')
    def test_get_modality_without_error(self, get_modality_mock):
        modality_id = 1
        get_modality_mock.return_value = ModalityOut(modality='url', id=modality_id)
        response = Response()
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router.get_modality(modality_id, response))

        self.assertEqual(result, ModalityOut(modality='url', id=modality_id, links=get_links(router)))
        get_modality_mock.assert_called_once_with(modality_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ModalityService, 'get_modality')
    def test_get_modality_with_error(self, get_modality_mock):
        get_modality_mock.return_value = ModalityOut(modality='url', errors={'errors': ['test']})
        response = Response()
        modality_id = 1
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router.get_modality(modality_id, response))

        self.assertEqual(result, ModalityOut(modality='url', errors={'errors': ['test']},  links=get_links(router)))
        get_modality_mock.assert_called_once_with(modality_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ModalityService, 'get_modalities')
    def test_get_modality_nodes_without_error(self, get_modalities_mock):
        get_modalities_mock.return_value = ModalitiesOut(modalities=[
            BasicModalityOut(modality='url', id=1), BasicModalityOut(modality='url2', id=2)])
        response = Response()
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router.get_modalities(response))

        self.assertEqual(result, ModalitiesOut(modalities=[
            BasicModalityOut(modality='url', id=1), BasicModalityOut(modality='url2', id=2)],
            links=get_links(router)))
        get_modalities_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
