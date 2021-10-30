from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut
from activity_execution.activity_execution_service import ActivityExecutionService

router = InferringRouter()


@cbv(router)
class ActivityExecutionRouter:
    """
    Class for routing activity_execution based requests

    Attributes:
        activity_execution_service (ActivityExecutionService): Service instance for activity execution
    """
    activity_execution_service = ActivityExecutionService()

    @router.post("/activity_execution", tags=["activity execution"], response_model=ActivityExecutionOut)
    async def create_activity_execution(self, activity_execution: ActivityExecutionIn, response: Response):
        """
        Create activity_execution in database
        """
        create_response = self.activity_execution_service.save_activity_execution(activity_execution)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
