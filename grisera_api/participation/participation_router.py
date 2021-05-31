from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from participation.participation_model import ParticipationsIn, ParticipationsOut
from participation.participation_service import ParticipationService

router = InferringRouter()


@cbv(router)
class ParticipationRouter:
    """
    Class for routing participation based requests

    Attributes:
        participation_service (ParticipationService): Service instance for participations
    """
    participation_service = ParticipationService()

    @router.post("/participations", tags=["participations"], response_model=ParticipationsOut)
    async def create_participations(self, participations: ParticipationsIn, response: Response):
        """
        Create participations in database
        """
        create_response = self.participation_service.save_participations(participations)

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
