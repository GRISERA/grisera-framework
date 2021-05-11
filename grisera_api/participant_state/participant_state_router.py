from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from participant_state.participant_state_model import ParticipantStateIn, ParticipantStateOut
from participant_state.participant_state_service import ParticipantStateService

router = InferringRouter()


@cbv(router)
class ParticipantStateRouter:
    """
    Class for routing participant state based requests

    Attributes:
        participant_state_service (ParticipantStateService): Service instance for participants' states
    """
    participant_state_service = ParticipantStateService()

    @router.post("/participant_state", tags=["participant state"], response_model=ParticipantStateOut)
    async def create_participant_state(self, participant_state: ParticipantStateIn, response: Response):
        """
        Create participant state in database
        """

        if participant_state.participant is not None and participant_state.participant.date_of_birth is not None:
            participant_state.participant.date_of_birth = participant_state.participant.date_of_birth.__str__()

        create_response = self.participant_state_service.save_participant_state(participant_state)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
