from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, BasicArrangementOut, ArrangementsOut
from arrangement.arrangement_service import ArrangementService
from models.not_found_model import NotFoundByIdModel

router = InferringRouter()


@cbv(router)
class ArrangementRouter:
    """
    Class for routing arrangement based requests

    Attributes:
    arrangement_service (ArrangementService): Service instance for arrangement
    """
    arrangement_service = None

    # dependency injection in the constructor
    def __init__(self, arrangement_service):
        self.arrangement_service = arrangement_service

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