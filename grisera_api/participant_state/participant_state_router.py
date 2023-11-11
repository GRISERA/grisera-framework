from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from participant_state.participant_state_model import (
    ParticipantStateIn,
    ParticipantStatesOut,
    ParticipantStateOut,
    ParticipantStatePropertyIn,
    ParticipantStateRelationIn,
)
from typing import Union
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class ParticipantStateRouter:
    """
    Class for routing participant state based requests

    Attributes:
        participant_state_service (ParticipantStateService): Service instance for participants' states
    """

    def __init__(self):
        self.participant_state_service = Services().participant_state_service()

    @router.post(
        "/participant_state",
        tags=["participant state"],
        response_model=ParticipantStateOut,
    )
    async def create_participant_state(
        self, participant_state: ParticipantStateIn, response: Response
    ):
        """
        Create participant state in database
        """

        create_response = self.participant_state_service.save_participant_state(
            participant_state
        )
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get(
        "/participant_state",
        tags=["participant state"],
        response_model=ParticipantStatesOut,
    )
    async def get_participant_states(self, response: Response):
        """
        Get participant states from database
        """

        get_response = self.participant_state_service.get_participant_states()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/participant_state/{participant_state_id}",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def get_participant_state(
        self, participant_state_id: Union[int, str], response: Response, depth: int=0
    ):
        """
        Get participant state from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """

        get_response = self.participant_state_service.get_participant_state(
            participant_state_id, depth
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/participant_state/{participant_state_id}",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def delete_participant_state(
        self, participant_state_id: Union[int, str], response: Response
    ):
        """
        Delete participant state from database
        """
        get_response = self.participant_state_service.delete_participant_state(
            participant_state_id
        )
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/participant_state/{participant_state_id}",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def update_participant_state(
        self,
        participant_state_id: Union[int, str],
        participant_state: ParticipantStatePropertyIn,
        response: Response,
    ):
        """
        Update participant state model in database
        """
        update_response = self.participant_state_service.update_participant_state(
            participant_state_id, participant_state
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/participant_state/{participant_state_id}/relationships",
        tags=["participant state"],
        response_model=Union[ParticipantStateOut, NotFoundByIdModel],
    )
    async def update_participant_state_relationships(
        self,
        participant_state_id: Union[int, str],
        participant_state: ParticipantStateRelationIn,
        response: Response,
    ):
        """
        Update participant state relations in database
        """
        update_response = (
            self.participant_state_service.update_participant_state_relationships(
                participant_state_id, participant_state
            )
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
