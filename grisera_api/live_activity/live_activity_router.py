from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from live_activity.live_activity_model import LiveActivityIn, LiveActivityOut, BasicLiveActivityOut, LiveActivitiesOut
from live_activity.live_activity_service import LiveActivityService
from models.not_found_model import NotFoundByIdModel

router = InferringRouter()


@cbv(router)
class LiveActivityRouter:
    """
    Class for routing live activity based requests

    Attributes:
    live_activity_service (LiveActivityService): Service instance for live activity
    """
    live_activity_service = LiveActivityService()

    @router.get("/live_activities/{live_activity_id}", tags=["live activities"],
                response_model=Union[LiveActivityOut, NotFoundByIdModel])
    async def get_live_activity(self, live_activity_id: int, response: Response):
        """
        Get live activity from database
        """
        get_response = self.live_activity_service.get_live_activity(live_activity_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/live_activities", tags=["live activities"], response_model=LiveActivitiesOut)
    async def get_live_activities(self, response: Response):
        """
        Get live activities from database
        """

        get_response = self.live_activity_service.get_live_activities()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
