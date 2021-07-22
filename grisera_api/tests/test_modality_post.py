from modality.modality_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_modality(*args, **kwargs):
    modality_out = ModalityOut(modality="body posture", id=1)
    return modality_out


class TestModalityPost(unittest.TestCase):

    @mock.patch.object(ModalityService, 'save_modality')
    def test_modality_post_without_error(self, mock_service):
        mock_service.side_effect = return_modality
        response = Response()
        modality = ModalityIn(modality="body posture")
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router
                             .create_modality(modality, response))

        self.assertEqual(result, ModalityOut(modality="body posture", id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ModalityService, 'save_modality')
    def test_modality_post_with_error(self, mock_service):
        mock_service.return_value = ModalityOut(modality="body posture", errors={'errors': ['test']})
        response = Response()
        modality = ModalityIn(modality="body posture")
        modality_router = ModalityRouter()

        result = asyncio.run(modality_router
                             .create_modality(modality, response))

        self.assertEqual(response.status_code, 422)
