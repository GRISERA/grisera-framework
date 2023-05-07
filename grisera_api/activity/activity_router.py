from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from activity.activity_model import ActivityOut, ActivitiesOut
from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class ActivityRouter:
    """
    Class for routing activity based requests

    Attributes:
        activity_service (ActivityService): Service instance for activity
    """

    def __init__(self):
        self.activity_service = Services().activity_service()

    @router.get(
        "/activities/{activity_id}",
        tags=["activities"],
        response_model=Union[ActivityOut, NotFoundByIdModel],
    )
    async def get_activity(
        self,
        activity_id: Union[int, str],
        response: Response,
        depth: int = 0,
    ):
        """
        Get activity from database. Depth attribute specifies how many models will be traversed to create the response.
        """
        get_response = self.activity_service.get_activity(activity_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/activities", tags=["activities"], response_model=ActivitiesOut)
    async def get_activities(self, response: Response):
        """
        Get activities from database
        """

        get_response = self.activity_service.get_activities()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
