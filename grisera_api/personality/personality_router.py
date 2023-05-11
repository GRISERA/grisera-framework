from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from personality.personality_model import (
    PersonalityBigFiveIn,
    PersonalityBigFiveOut,
    PersonalityPanasIn,
    PersonalityPanasOut,
    PersonalitiesOut,
)

from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class PersonalityRouter:
    """
    Class for routing personality based requests

    Attributes:
        personality_service (PersonalityService): Service instance for personality
    """

    def __init__(self):
        self.personality_service = Services().personality_service()


    @router.post(
        "/personality/big_five_model",
        tags=["personality"],
        response_model=PersonalityBigFiveOut,
    )
    async def create_personality_big_five(
        self, personality: PersonalityBigFiveIn, response: Response, dataset_name: str
    ):
        """
        Create personality big five model in database
        """

        create_response = self.personality_service.save_personality_big_five(
            personality,dataset_name
        )

        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response


    @router.post(
        "/personality/panas_model",
        tags=["personality"],
        response_model=PersonalityPanasOut,
    )
    async def create_personality_panas(
        self, personality: PersonalityPanasIn, response: Response, dataset_name: str
    ):
        """
        Create personality panas model in database
        """

        create_response = self.personality_service.save_personality_panas(personality, dataset_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response


    @router.get(
        "/personality/{personality_id}",
        tags=["personality"],
        response_model=Union[
            PersonalityBigFiveOut, PersonalityPanasOut, NotFoundByIdModel
        ],
    )
    async def get_personality(
        self, personality_id: Union[int, str], response: Response, dataset_name: str, depth: int=0
    ):

        """
        Get personality from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.personality_service.get_personality(personality_id,dataset_name, depth)

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/personality", tags=["personality"], response_model=PersonalitiesOut)
    async def get_personalities(self, response: Response, dataset_name: str):
        """
        Get personalities from database
        """

        get_response = self.personality_service.get_personalities(dataset_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response


    @router.delete(
        "/personality/{personality_id}",
        tags=["personality"],
        response_model=Union[
            PersonalityBigFiveOut, PersonalityPanasOut, NotFoundByIdModel
        ],
    )
    async def delete_personality(
        self, personality_id: Union[int, str], response: Response, dataset_name: str
    ):
        """
        Delete personality from database
        """
        get_response = self.personality_service.delete_personality(personality_id, dataset_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/personality/big_five_model/{personality_id}",
        tags=["personality"],
        response_model=Union[PersonalityBigFiveOut, NotFoundByIdModel],
    )
    async def update_personality_big_five(
        self,
        personality_id: Union[int, str],
        personality: PersonalityBigFiveIn,
        response: Response, dataset_name: str
    ):
        """
        Update personality big five model in database
        """
        update_response = self.personality_service.update_personality_big_five(
            personality_id, personality,dataset_name
        )

        if update_response.errors is not None:
            response.status_code = (
                404 if type(update_response) == NotFoundByIdModel else 422
            )

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/personality/panas_model/{personality_id}",
        tags=["personality"],
        response_model=Union[PersonalityPanasOut, NotFoundByIdModel],
    )
    async def update_personality_panas(
        self,
        personality_id: Union[int, str],
        personality: PersonalityPanasIn,
        response: Response, dataset_name: str
    ):
        """
        Update personality panas model in database
        """
        update_response = self.personality_service.update_personality_panas(
            personality_id, personality,dataset_name
        )

        if update_response.errors is not None:
            response.status_code = (
                404 if type(update_response) == NotFoundByIdModel else 422
            )

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
