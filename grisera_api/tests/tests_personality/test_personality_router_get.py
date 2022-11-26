import asyncio
import unittest
import unittest.mock as mock
from personality.personality_router import *
from personality.personality_service_graphdb import PersonalityServiceGraphDB


class TestPersonalityRouterGet(unittest.TestCase):

    @mock.patch.object(PersonalityServiceGraphDB, 'get_personality')
    def test_get_personality_without_error(self, get_personality_mock):
        personality_id = 1
        get_personality_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                  extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                                  id=personality_id)
        response = Response()
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.get_personality(personality_id, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                       extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                       id=personality_id, links=get_links(router)))
        get_personality_mock.assert_called_once_with(personality_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PersonalityServiceGraphDB, 'get_personality')
    def test_get_personality_with_error(self, get_personality_mock):
        get_personality_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                  extroversion=2.5, neuroticism=2.5, openess=2.5,
                                                                  errors={'errors': ['test']})
        response = Response()
        personality_id = 1
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.get_personality(personality_id, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                       neuroticism=2.5, openess=2.5, errors={'errors': ['test']},
                                                       links=get_links(router)))
        get_personality_mock.assert_called_once_with(personality_id)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(PersonalityServiceGraphDB, 'get_personalities')
    def test_get_personalities_without_error(self, get_personalities_mock):
        get_personalities_mock.return_value = PersonalitiesOut(personalities=[
            BasicPersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5, neuroticism=2.5,
                                       openess=2.5, id=1),
            BasicPersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5, neuroticism=2.5,
                                       openess=2.5, id=2)])
        response = Response()
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.get_personalities(response))

        self.assertEqual(result, PersonalitiesOut(personalities=[
            BasicPersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5, neuroticism=2.5,
                                       openess=2.5, id=1),
            BasicPersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5, neuroticism=2.5,
                                       openess=2.5, id=2)],
            links=get_links(router)))
        get_personalities_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
