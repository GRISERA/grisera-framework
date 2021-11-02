import asyncio
import unittest
import unittest.mock as mock
from personality.personality_router import *


class TestPersonalityRouter(unittest.TestCase):

    @mock.patch.object(PersonalityService, 'save_personality_big_five')
    def test_create_personality_big_five_without_error(self, save_personality_big_five_mock):
        save_personality_big_five_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                            extroversion=2.5, neuroticism=2.5,
                                                                            openess=2.5, id=1)
        response = Response()
        personality = PersonalityBigFiveIn(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                           neuroticism=2.5, openess=2.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.create_personality_big_five(personality, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                       extroversion=2.5,neuroticism=2.5, openess=2.5,
                                                       id=1, links=get_links(router)))
        save_personality_big_five_mock.assert_called_once_with(personality)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PersonalityService, 'save_personality_big_five')
    def test_create_personality_big_five_with_error(self, save_personality_big_five_mock):
        save_personality_big_five_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                            extroversion=2.5, neuroticism=2.5,
                                                                            openess=2.5, errors={'errors': ['test']})
        response = Response()
        personality = PersonalityBigFiveIn(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                           neuroticism=2.5, openess=2.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.create_personality_big_five(personality, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                       neuroticism=2.5, openess=2.5, errors={'errors': ['test']},
                                                       links=get_links(router)))
        save_personality_big_five_mock.assert_called_once_with(personality)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(PersonalityService, 'save_personality_panas')
    def test_create_personality_panas_without_error(self, save_personality_panas_mock):
        save_personality_panas_mock.return_value = PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=1)
        response = Response()
        personality = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.create_personality_panas(personality, response))

        self.assertEqual(result, PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=1,
                                                     links=get_links(router)))
        save_personality_panas_mock.assert_called_once_with(personality)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PersonalityService, 'save_personality_panas')
    def test_create_personality_panas_with_error(self, save_personality_panas_mock):
        save_personality_panas_mock.return_value = PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5,
                                                                       errors={'errors': ['test']})
        response = Response()
        personality = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.create_personality_panas(personality, response))

        self.assertEqual(result, PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5,
                                                     errors={'errors': ['test']}, links=get_links(router)))
        save_personality_panas_mock.assert_called_once_with(personality)
        self.assertEqual(response.status_code, 422)
