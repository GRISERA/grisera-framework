from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from activity.activity_model import ActivityIn, ActivityOut
from activity.activity_service import ActivityService

router = InferringRouter()


@cbv(router)
class ActivityRouter:
    """
    Class for routing activity based requests

    Attributes:
        activity_service (ActivityService): Service instance for activities
    """
    activity_service = ActivityService()

    @router.post("/activities", tags=["activities"], response_model=ActivityOut)
    async def create_activity(self, activity: ActivityIn, response: Response):
        """
        Create activity in database
        """
        create_response = self.activity_service.save_activity(activity)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
