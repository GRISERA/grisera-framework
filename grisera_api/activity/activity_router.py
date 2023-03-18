from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from activity.activity_model import ActivityOut, ActivitiesOut, ActivityIn
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

    @router.post("/activities", tags=["activities"], response_model=ActivityOut)
    async def create_activity(self, activity: ActivityIn, response: Response, database_name: str):
        """
        Create activity in database
        """
        create_response = self.activity_service.save_activity(activity, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
    
    @router.get("/activities/{activity_id}", tags=["activities"],
                response_model=Union[ActivityOut, NotFoundByIdModel])
    async def get_activity(self, activity_id: int, response: Response, database_name: str):
        """
        Get activity from database
        """
        get_response = self.activity_service.get_activity(activity_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/activities", tags=["activities"], response_model=ActivitiesOut)
    async def get_activities(self, response: Response, database_name: str):
        """
        Get activities from database
        """

        get_response = self.activity_service.get_activities(database_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/activities/{activity_id}", tags=["activities"],
                   response_model=Union[ActivityOut, NotFoundByIdModel])
    async def delete_activity(self, activity_id: int, response: Response, database_name: str):
        """
        Delete activity from database
        """
        get_response = self.activity_service.delete_activity(activity_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/activities/{activity_id}", tags=["activities"],
                response_model=Union[ActivityOut, NotFoundByIdModel])
    async def update_activity(self, activity_id: int, activity: ActivityIn, response: Response, database_name: str):
        """
        Update activity model in database
        """
        update_response = self.activity_service.update_activity(activity_id, activity, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
