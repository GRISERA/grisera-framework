import asyncio
import unittest
import unittest.mock as mock
from life_activity.life_activity_router import *
from life_activity.life_activity_model import BasicLifeActivityOut
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from property.property_model import PropertyIn


class TestLifeActivityRouterGet(unittest.TestCase):

    @mock.patch.object(LifeActivityServiceGraphDB, 'get_life_activity')
    def test_get_life_activity_without_error(self, get_life_activity_mock):
        dataset_name = "neo4j"
        life_activity_id = 1
        get_life_activity_mock.return_value = LifeActivityOut(life_activity='url', id=life_activity_id)
        response = Response()
        life_activity_router = LifeActivityRouter()

        result = asyncio.run(life_activity_router.get_life_activity(life_activity_id, response, dataset_name))

        self.assertEqual(result, LifeActivityOut(life_activity='url', id=life_activity_id, links=get_links(router)))
        get_life_activity_mock.assert_called_once_with(life_activity_id, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(LifeActivityServiceGraphDB, 'get_life_activity')
    def test_get_life_activity_with_error(self, get_life_activity_mock):
        dataset_name = "neo4j"
        get_life_activity_mock.return_value = LifeActivityOut(life_activity='url', errors={'errors': ['test']})
        response = Response()
        life_activity_id = 1
        life_activity_router = LifeActivityRouter()

        result = asyncio.run(life_activity_router.get_life_activity(life_activity_id, response, dataset_name))

        self.assertEqual(result, LifeActivityOut(life_activity='url', errors={'errors': ['test']},  links=get_links(router)))
        get_life_activity_mock.assert_called_once_with(life_activity_id, dataset_name)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(LifeActivityServiceGraphDB, 'get_life_activities')
    def test_get_life_activity_nodes_without_error(self, get_life_activities_mock):
        dataset_name = "neo4j"
        get_life_activities_mock.return_value = LifeActivitiesOut(life_activities=[
            BasicLifeActivityOut(life_activity='url', id=1), BasicLifeActivityOut(life_activity='url2', id=2)])
        response = Response()
        life_activity_router = LifeActivityRouter()

        result = asyncio.run(life_activity_router.get_life_activities(response, dataset_name))

        self.assertEqual(result, LifeActivitiesOut(life_activities=[
            BasicLifeActivityOut(life_activity='url', id=1), BasicLifeActivityOut(life_activity='url2', id=2)],
            links=get_links(router)))
        get_life_activities_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
