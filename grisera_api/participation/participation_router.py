from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from participation.participation_model import ParticipationIn, ParticipationOut, ParticipationsOut
from participation.participation_service import ParticipationService
from services import Services

router = InferringRouter()


@cbv(router)
class ParticipationRouter:
    """
    Class for routing participation based requests

    Attributes:
        participation_service (ParticipationService): Service instance for participation
    """

    def __init__(self):
        self.participation_service = Services().participation_service()

    @router.post("/participations", tags=["participations"], response_model=ParticipationOut)
    async def create_participation(self, participation: ParticipationIn, response: Response):
        """
        Create participation in database
        """
        create_response = self.participation_service.save_participation(participation)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/participations", tags=["participations"], response_model=ParticipationsOut)
    async def get_participations(self, response: Response):
        """
        Get participations from database
        """

        get_response = self.participation_service.get_participations()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/participations/{participation_id}", tags=["participations"],
                response_model=Union[ParticipationOut, NotFoundByIdModel])
    async def get_participation(self, participation_id: int, response: Response):
        """
        Get participations from database
        """

        get_response = self.participation_service.get_participation(participation_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/participations/{participation_id}", tags=["participations"],
                   response_model=Union[ParticipationOut, NotFoundByIdModel])
    async def delete_participation(self, participation_id: int, response: Response):
        """
        Delete participations from database
        """
        get_response = self.participation_service.delete_participation(participation_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/participations/{participation_id}/relationships", tags=["participations"],
                response_model=Union[ParticipationOut, NotFoundByIdModel])
    async def update_participation_relationships(self, participation_id: int, participation: ParticipationIn,
                                                 response: Response):
        """
        Update participations relations in database
        """
        update_response = self.participation_service.update_participation_relationships(participation_id, participation)

        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
