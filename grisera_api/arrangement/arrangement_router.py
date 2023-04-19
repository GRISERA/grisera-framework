from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from arrangement.arrangement_model import ArrangementIn, ArrangementOut, ArrangementsOut
from arrangement.arrangement_service import ArrangementService
from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class ArrangementRouter:
    """
    Class for routing arrangement based requests

    Attributes:
        arrangement_service (ArrangementService): Service instance for arrangement
    """

    def __init__(self):
        self.arrangement_service = Services().arrangement_service()

    @router.post("/arrangements", tags=["arrangements"], response_model=ArrangementOut)
    async def create_arrangement(self, arrangement: ArrangementIn, response: Response):
        """
        Create arrangement in database
        """

        create_response = self.arrangement_service.save_arrangement(arrangement)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/arrangements/{arrangement_id}", tags=["arrangements"],
                response_model=Union[ArrangementOut, NotFoundByIdModel])
    async def get_arrangement(self, arrangement_id: int, response: Response):
        """
        Get arrangement from database
        """
        get_response = self.arrangement_service.get_arrangement(arrangement_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/arrangements", tags=["arrangements"], response_model=ArrangementsOut)
    async def get_arrangements(self, response: Response):
        """
        Get arrangements from database
        """

        get_response = self.arrangement_service.get_arrangements()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response