from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from live_activity.live_activity_model import LiveActivityIn, LiveActivityOut
from live_activity.live_activity_service import LiveActivityService

router = InferringRouter()


@cbv(router)
class LiveActivityRouter:
    """
    Class for routing live activity based requests

    Attributes:
        live_activity_service (LiveActivityService): Service instance for live activity
    """
    live_activity_service = LiveActivityService()

    @router.post("/live_activity", tags=["live activity"], response_model=LiveActivityOut)
    async def create_live_activity(self, live_activity: LiveActivityIn, response: Response):
        """
        Create live activity in database
        """
        create_response = self.live_activity_service.save_live_activity(live_activity)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
