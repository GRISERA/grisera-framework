from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from participation.participation_model import ParticipationIn, ParticipationOut
from participation.participation_service import ParticipationService

router = InferringRouter()


@cbv(router)
class ParticipationRouter:
    """
    Class for routing participation based requests

    Attributes:
        participation_service (ParticipationService): Service instance for participation
    """
    participation_service = ParticipationService()

    @router.post("/participation", tags=["participation"], response_model=ParticipationOut)
    async def create_participation(self, response: Response):
        """
        Create participation in database
        """
        create_response = self.participation_service.save_participation()
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
