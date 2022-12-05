import asyncio
import unittest
import unittest.mock as mock
from personality.personality_router import *
from personality.personality_service_graphdb import PersonalityServiceGraphDB


class TestPersonalityRouterPut(unittest.TestCase):

    @mock.patch.object(PersonalityServiceGraphDB, 'update_personality_big_five')
    def test_update_appearance_occlusion_without_error(self, update_personality_big_five_mock):
        personality_id = 1
        update_personality_big_five_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                              extroversion=2.5, neuroticism=2.5,
                                                                              openess=2.5, id=personality_id)
        response = Response()
        personality = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                            extroversion=2.5, neuroticism=2.5, openess=2.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.update_personality_big_five(personality_id, personality, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                       neuroticism=2.5, openess=2.5, id=personality_id,
                                                       links=get_links(router)))
        update_personality_big_five_mock.assert_called_once_with(personality_id, personality)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PersonalityServiceGraphDB, 'update_personality_big_five')
    def test_update_personality_big_five_with_error(self, update_personality_big_five_mock):
        personality_id = 1
        update_personality_big_five_mock.return_value = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                                                              extroversion=2.5, neuroticism=2.5,
                                                                              openess=2.5, errors={'errors': ['test']})
        response = Response()
        personality = PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5,
                                            extroversion=2.5, neuroticism=2.5, openess=2.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.update_personality_big_five(personality_id, personality, response))

        self.assertEqual(result, PersonalityBigFiveOut(agreeableness=2.5, conscientiousness=2.5, extroversion=2.5,
                                                       neuroticism=2.5, openess=2.5, errors={'errors': ['test']},
                                                       links=get_links(router)))
        update_personality_big_five_mock.assert_called_once_with(personality_id, personality)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(PersonalityServiceGraphDB, 'update_personality_panas')
    def test_update_personality_panas_without_error(self, update_personality_panas_mock):
        personality_id = 1
        update_personality_panas_mock.return_value = PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5,
                                                                         id=personality_id)
        response = Response()
        personality = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.update_personality_panas(personality_id, personality, response))

        self.assertEqual(result, PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5, id=personality_id,
                                                     links=get_links(router)))
        update_personality_panas_mock.assert_called_once_with(personality_id, personality)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PersonalityServiceGraphDB, 'update_personality_panas')
    def test_update_personality_panas_with_error(self, update_personality_panas_mock):
        update_personality_panas_mock.return_value = PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5,
                                                                         errors={'errors': ['test']})
        response = Response()
        personality_id = 1
        personality = PersonalityPanasIn(negative_affect=0.5, positive_affect=0.5)
        personality_router = PersonalityRouter()

        result = asyncio.run(personality_router.update_personality_panas(personality_id, personality, response))

        self.assertEqual(result, PersonalityPanasOut(negative_affect=0.5, positive_affect=0.5,
                                                     errors={'errors': ['test']}, links=get_links(router)))
        update_personality_panas_mock.assert_called_once_with(personality_id, personality)
        self.assertEqual(response.status_code, 422)
