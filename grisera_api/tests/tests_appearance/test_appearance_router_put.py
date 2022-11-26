import asyncio
import unittest
import unittest.mock as mock
from appearance.appearance_router import *
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB


class TestAppearanceRouterPut(unittest.TestCase):

    @mock.patch.object(AppearanceServiceGraphDB, 'update_appearance_occlusion')
    def test_update_appearance_occlusion_without_error(self, update_appearance_occlusion_mock):
        appearance_id = 1
        update_appearance_occlusion_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                                               id=appearance_id)
        response = Response()
        appearance = AppearanceOcclusionIn(glasses=False, beard="Heavy", moustache="Heavy")
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.update_appearance_occlusion(appearance_id, appearance, response))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                        id=appearance_id, links=get_links(router)))
        update_appearance_occlusion_mock.assert_called_once_with(appearance_id, appearance)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AppearanceServiceGraphDB, 'update_appearance_occlusion')
    def test_update_appearance_occlusion_with_error(self, update_appearance_occlusion_mock):
        appearance_id = 1
        update_appearance_occlusion_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                                               errors={'errors': ['test']})
        response = Response()
        appearance = AppearanceOcclusionIn(glasses=False, beard="Heavy", moustache="Heavy")
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.update_appearance_occlusion(appearance_id, appearance, response))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", errors={'errors': ['test']},
                                                        links=get_links(router)))
        update_appearance_occlusion_mock.assert_called_once_with(appearance_id, appearance)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(AppearanceServiceGraphDB, 'update_appearance_somatotype')
    def test_update_appearance_somatotype_without_error(self, update_appearance_somatotype_mock):
        appearance_id = 1
        update_appearance_somatotype_mock.return_value = AppearanceSomatotypeOut(ectomorph=2.7,
                                                                                 endomorph=1.6, mesomorph=3.8,
                                                                                 id=appearance_id)
        response = Response()
        appearance = AppearanceSomatotypeIn(ectomorph=2.7, endomorph=1.6, mesomorph=3.8)
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.update_appearance_somatotype(appearance_id, appearance, response))

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=2.7, endomorph=1.6, mesomorph=3.8,
                                                         id=appearance_id, links=get_links(router)))
        update_appearance_somatotype_mock.assert_called_once_with(appearance_id, appearance)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AppearanceServiceGraphDB, 'update_appearance_somatotype')
    def test_update_appearance_somatotype_with_error(self, update_appearance_somatotype_mock):
        update_appearance_somatotype_mock.return_value = AppearanceSomatotypeOut(ectomorph=2.7,
                                                                                 endomorph=1.6, mesomorph=3.8,
                                                                                 errors={'errors': ['test']})
        response = Response()
        appearance_id = 1
        appearance = AppearanceSomatotypeIn(ectomorph=2.7, endomorph=1.6, mesomorph=3.8)
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.update_appearance_somatotype(appearance_id, appearance, response))

        self.assertEqual(result, AppearanceSomatotypeOut(ectomorph=2.7, endomorph=1.6, mesomorph=3.8,
                                                        errors={'errors': ['test']}, links=get_links(router)))
        update_appearance_somatotype_mock.assert_called_once_with(appearance_id, appearance)
        self.assertEqual(response.status_code, 422)
