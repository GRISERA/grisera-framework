import asyncio
import unittest
import unittest.mock as mock
from appearance.appearance_router import *
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB


class TestAppearanceRouterDelete(unittest.TestCase):

    @mock.patch.object(AppearanceServiceGraphDB, 'delete_appearance')
    def test_delete_appearance_without_error(self, delete_appearance_mock):
        database_name = "neo4j"
        appearance_id = 1
        delete_appearance_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", id=appearance_id)
        response = Response()
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.delete_appearance(appearance_id, response, database_name))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                        id=appearance_id, links=get_links(router)))
        delete_appearance_mock.assert_called_once_with(appearance_id, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AppearanceServiceGraphDB, 'delete_appearance')
    def test_delete_appearance_with_error(self, delete_appearance_mock):
        database_name = "neo4j"
        delete_appearance_mock.return_value = AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy",
                                                                     errors={'errors': ['test']})
        response = Response()
        appearance_id = 1
        appearance_router = AppearanceRouter()

        result = asyncio.run(appearance_router.delete_appearance(appearance_id, response, database_name))

        self.assertEqual(result, AppearanceOcclusionOut(glasses=False, beard="Heavy", moustache="Heavy", errors={'errors': ['test']},
                                                        links=get_links(router)))
        delete_appearance_mock.assert_called_once_with(appearance_id, database_name)
        self.assertEqual(response.status_code, 404)
