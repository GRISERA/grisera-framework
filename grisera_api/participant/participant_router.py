from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.encoders import jsonable_encoder
from hateoas import get_links
from participant.participant_model import ParticipantIn, ParticipantOut
from participant.participant_service import ParticipantService

router = InferringRouter()


@cbv(router)
class ParticipantRouter:
    """
    Class for routing participant based requests

    Attributes:
        participant_service (ParticipantService): Service instance for participants
    """
    participant_service = ParticipantService()

    @router.post("/participants", tags=["participants"], response_model=ParticipantOut)
    async def create_participant(self, participant: ParticipantIn, response: Response):
        """
        Create participant in database
        """

        if participant.date_of_birth is not None:
            participant.date_of_birth = participant.date_of_birth.__str__()

        create_response = self.participant_service.save_participant(participant)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
