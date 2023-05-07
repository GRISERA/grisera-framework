from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, BasicArrangementOut, ArrangementsOut
from arrangement.arrangement_service import ArrangementService
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

    @router.get("/arrangements/{arrangement_id}", tags=["arrangements"],
                response_model=Union[ArrangementOut, NotFoundByIdModel])
    async def get_arrangement(self, arrangement_id: int, response: Response, database_name: str):
        """
        Get arrangement from database
        """
        get_response = self.arrangement_service.get_arrangement(arrangement_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/arrangements", tags=["arrangements"], response_model=ArrangementsOut)
    async def get_arrangements(self, response: Response, database_name: str):
        """
        Get arrangements from database
        """

        get_response = self.arrangement_service.get_arrangements(database_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.post("/arrangements", tags=["arrangements"], response_model=ArrangementsOut)
    async def create_activity(self, arrangement: ArrangementIn, response: Response, database_name: str):
        """
        Create arrangement in database
        """
        create_response = self.arrangement_service.save_arrangement(arrangement, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.delete("/arrangements/{arrangement_id}", tags=["arrangements"],
                   response_model=Union[ArrangementOut, NotFoundByIdModel])
    async def delete_arrangement(self, arrangement_id: int, response: Response, database_name: str):
        """
        Delete arrangement from database
        """
        get_response = self.arrangement_service.delete_arrangement(arrangement_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/arrangements/{arrangement_id}", tags=["arrangements"],
                response_model=Union[ArrangementOut, NotFoundByIdModel])
    async def update_activity(self, arrangement_id: int, arrangement: ArrangementIn, response: Response, database_name: str):
        """
        Update arrangement model in database
        """
        update_response = self.arrangement_service.update_arrangement(arrangement_id, arrangement, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response