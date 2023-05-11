from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from life_activity.life_activity_model import (
    LifeActivityOut,
    LifeActivitiesOut,
)
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class LifeActivityRouter:
    """
    Class for routing life activity based requests

    Attributes:
        life_activity_service (LifeActivityService): Service instance for life activity
    """

    def __init__(self):
        self.life_activity_service = Services().life_activity_service()


    @router.get(
        "/life_activities/{life_activity_id}",
        tags=["life activities"],
        response_model=Union[LifeActivityOut, NotFoundByIdModel],
    )
    async def get_life_activity(
        self, life_activity_id: Union[int, str], response: Response, dataset_name: str, depth: int = 0
    ):

        """
        Get life activity from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.life_activity_service.get_life_activity(
            life_activity_id, dataset_name, depth
        )

        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response


    @router.get(
        "/life_activities", tags=["life activities"], response_model=LifeActivitiesOut
    )
    async def get_life_activities(self, response: Response, dataset_name: str):

        """
        Get life activities from database
        """

        get_response = self.life_activity_service.get_life_activities(dataset_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
