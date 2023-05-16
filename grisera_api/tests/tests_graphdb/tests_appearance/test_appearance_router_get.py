import asyncio
import unittest
import unittest.mock as mock

from appearance.appearance_model import BasicAppearanceOcclusionOut, BasicAppearanceSomatotypeOut
from appearance.appearance_router import *
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB


class TestAppearanceRouterGet(unittest.TestCase):

    @mock.patch.object(AppearanceServiceGraphDB, 'get_appearance')
    def test_get_appearance_without_error(self, get_appearance_mock):
        appearance_id = 1
        get_appearance_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                                  id=appearance_id)
        response = Response()
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.get_appearance(appearance_id, response))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                        id=appearance_id, links=get_links(router)))
        get_appearance_mock.assert_called_once_with(appearance_id, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AppearanceServiceGraphDB, 'get_appearance')
    def test_get_appearance_with_error(self, get_appearance_mock):
        get_appearance_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                                  errors={'errors': ['test']})
        response = Response()
        appearance_id = 1
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.get_appearance(appearance_id, response))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                        errors={'errors': ['test']},
                                                        links=get_links(router)))
        get_appearance_mock.assert_called_once_with(appearance_id, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(AppearanceServiceGraphDB, 'get_appearances')
    def test_get_appearances_without_error(self, get_appearances_mock):
        get_appearances_mock.return_value = AppearancesOut(appearances=[
            BasicAppearanceOcclusionOut(id=1, glasses=False, beard="Heavy", moustache="Heavy"),
            BasicAppearanceSomatotypeOut(id=2, ectomorph=2.7, endomorph=1.6, mesomorph=3.8)])
        response = Response()
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.get_appearances(response))

        self.assertEqual(result, AppearancesOut(appearances=[
            BasicAppearanceOcclusionOut(id=1, glasses=False, beard="Heavy", moustache="Heavy"),
            BasicAppearanceSomatotypeOut(id=2, ectomorph=2.7, endomorph=1.6, mesomorph=3.8)],
            links=get_links(router)))
        get_appearances_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
