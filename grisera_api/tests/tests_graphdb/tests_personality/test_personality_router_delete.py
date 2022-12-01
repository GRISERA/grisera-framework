import asyncio
import unittest
import unittest.mock as mock
from personality.personality_router import *
from personality.personality_service_graphdb import PersonalityServiceGraphDB


class TestPersonalityRouterDelete(unittest.TestCase):

    @mock.patch.object(PersonalityServiceGraphDB, 'delete_personality')
    def test_delete_personality_without_error(self, delete_personality_mock):
        personality_id = 1
        delete_personality_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                     extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                                     id=personality_id)
        response = Response()
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.delete_personality(personality_id, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                       extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                       id=personality_id, links=get_links(router)))
        delete_personality_mock.assert_called_once_with(personality_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PersonalityServiceGraphDB, 'delete_personality')
    def test_delete_personality_with_error(self, delete_personality_mock):
        delete_personality_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                     extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                                     errors={'errors': ['test']})
        response = Response()
        personality_id = 1
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.delete_personality(personality_id, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                       extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                       errors={'errors': ['test']}, links=get_links(router)))
        delete_personality_mock.assert_called_once_with(personality_id)
        self.assertEqual(response.status_code, 404)
