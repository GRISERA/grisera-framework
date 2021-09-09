from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from personality.personality_model import PersonalityBigFiveIn, PersonalityBigFiveOut, \
    PersonalityPanasIn, PersonalityPanasOut
from personality.personality_service import PersonalityService

router = InferringRouter()


@cbv(router)
class PersonalityRouter:
    """
    Class for routing personality based requests

    Attributes:
        personality_service (PersonalityService): Service instance for personality
    """
    personality_service = PersonalityService()

    @router.post("/personality/big_five_model", tags=["personality"], response_model=PersonalityBigFiveOut)
    async def create_personality_big_five(self, personality: PersonalityBigFiveIn, response: Response):
        """
        Create personality big five model in database
        """

        create_response = self.personality_service.save_personality_big_five(personality)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/personality/panas_model", tags=["personality"], response_model=PersonalityPanasOut)
    async def create_personality_panas(self, personality: PersonalityPanasIn, response: Response):
        """
        Create personality panas model in database
        """

        create_response = self.personality_service.save_personality_panas(personality)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
