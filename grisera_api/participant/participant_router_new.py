from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from typing import Union
from participant.participant_model_new import (
    ParticipantIn,
    ParticipantOut,
    ParticipantsOut,
)
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class ParticipantRouter:
    """
    Class for routing participant based requests

    Attributes:
        participant_service (ParticipantService): Service instance for participants
    """

    def __init__(self):
        self.participant_service = Services().participant_service()

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

    @router.get("/participants", tags=["participants"], response_model=ParticipantsOut)
    async def get_participants(self, response: Response):
        """
        Get participants from database
        """

        get_response = self.participant_service.get_participants()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/participants/{participant_id}",
        tags=["participants"],
        response_model=Union[ParticipantOut, NotFoundByIdModel],
    )
    async def get_participant(
        self, participant_id: Union[str, int], response: Response
    ):
        """
        Get participant from database
        """

        get_response = self.participant_service.get_participant(participant_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/participants/{participant_id}",
        tags=["participants"],
        response_model=Union[ParticipantOut, NotFoundByIdModel],
    )
    async def delete_participant(self, participant_id: int, response: Response):
        """
        Delete participant from database
        """
        get_response = self.participant_service.delete_participant(participant_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/participants/{participant_id}",
        tags=["participants"],
        response_model=Union[ParticipantOut, NotFoundByIdModel],
    )
    async def update_participant(
        self, participant_id: int, participant: ParticipantIn, response: Response
    ):
        """
        Update participant model in database
        """
        update_response = self.participant_service.update_participant(
            participant_id, participant
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
