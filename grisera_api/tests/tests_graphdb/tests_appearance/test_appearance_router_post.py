import asyncio
import unittest
import unittest.mock as mock
from appearance.appearance_router import *
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB


class TestAppearanceRouterPost(unittest.TestCase):

    @mock.patch.object(AppearanceServiceGraphDB, 'save_appearance_occlusion')
    def test_create_appearance_occlusion_without_error(self, save_appearance_occlusion_mock):
        save_appearance_occlusion_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", id=1)
        response = Response()
        appearance = AppearanceOcclusionIn(glasses=False, beard="Heavy", moustache="Heavy")
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.create_appearance_occlusion(appearance, response))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", id=1, links=get_links(router)))
        save_appearance_occlusion_mock.assert_called_once_with(appearance)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AppearanceServiceGraphDB, 'save_appearance_occlusion')
    def test_create_appearance_occlusion_with_error(self, save_appearance_occlusion_mock):
        save_appearance_occlusion_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                                             errors={'errors': ['test']})
        response = Response()
        appearance = AppearanceOcclusionIn(glasses=False, beard="Heavy", moustache="Heavy")
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.create_appearance_occlusion(appearance, response))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", errors={'errors': ['test']},
                                                        links=get_links(router)))
        save_appearance_occlusion_mock.assert_called_once_with(appearance)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(AppearanceServiceGraphDB, 'save_appearance_somatotype')
    def test_create_appearance_somatotype_without_error(self, save_appearance_somatotype_mock):
        save_appearance_somatotype_mock.return_value = AppearanceSomatotypeOut(ectomorph=2.7,
                                                                               endomorph=1.6, mesomorph=3.8, id=1)
        response = Response()
        appearance = AppearanceSomatotypeIn(ectomorph=2.7, endomorph=1.6, mesomorph=3.8)
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.create_appearance_somatotype(appearance, response))

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=2.7, endomorph=1.6, mesomorph=3.8,
                                                         id=1, links=get_links(router)))
        save_appearance_somatotype_mock.assert_called_once_with(appearance)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AppearanceServiceGraphDB, 'save_appearance_somatotype')
    def test_create_appearance_somatotype_with_error(self, save_appearance_somatotype_mock):
        save_appearance_somatotype_mock.return_value = AppearanceSomatotypeOut(ectomorph=2.7,
                                                                               endomorph=1.6, mesomorph=3.8,
                                                                               errors={'errors': ['test']})
        response = Response()
        appearance = AppearanceSomatotypeIn(ectomorph=2.7, endomorph=1.6, mesomorph=3.8)
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.create_appearance_somatotype(appearance, response))

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=2.7, endomorph=1.6, mesomorph=3.8,
                                                        errors={'errors': ['test']}, links=get_links(router)))
        save_appearance_somatotype_mock.assert_called_once_with(appearance)
        self.assertEqual(response.status_code, 422)
