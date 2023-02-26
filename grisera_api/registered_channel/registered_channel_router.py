from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from registered_channel.registered_channel_model import RegisteredChannelIn, RegisteredChannelsOut, \
    RegisteredChannelOut
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from services import Services

router = InferringRouter()


@cbv(router)
class RegisteredChannelRouter:
    """
    Class for routing registered channel based requests

    Attributes:
        registered_channel (RegisteredChannelService): Service instance for registered channel
    """

    def __init__(self):
        self.registered_channel_service = Services().registered_channel_service()

    @router.post("/registered_channels", tags=["registered channels"], response_model=RegisteredChannelOut)
    async def create_registered_channel(self, registered_channel: RegisteredChannelIn, response: Response, database_name: str):
        """
        Create registered channel in database
        """
        create_response = self.registered_channel_service.save_registered_channel(registered_channel, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/registered_channels", tags=["registered channels"], response_model=RegisteredChannelsOut)
    async def get_registered_channels(self, response: Response, database_name: str):
        """
        Get registered channels from database
        """

        get_response = self.registered_channel_service.get_registered_channels(database_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/registered_channels/{registered_channel_id}", tags=["registered channels"],
                response_model=Union[RegisteredChannelOut, NotFoundByIdModel])
    async def get_registered_channel(self, registered_channel_id: int, response: Response, database_name: str):
        """
        Get registered channels from database
        """

        get_response = self.registered_channel_service.get_registered_channel(registered_channel_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/registered_channels/{registered_channel_id}", tags=["registered channels"],
                   response_model=Union[RegisteredChannelOut, NotFoundByIdModel])
    async def delete_registered_channel(self, registered_channel_id: int, response: Response, database_name: str):
        """
        Delete registered channels from database
        """
        get_response = self.registered_channel_service.delete_registered_channel(registered_channel_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/registered_channels/{registered_channel_id}/relationships", tags=["registered channels"],
                response_model=Union[RegisteredChannelOut, NotFoundByIdModel])
    async def update_registered_channel_relationships(self, registered_channel_id: int,
                                                      registered_channel: RegisteredChannelIn,
                                                      response: Response, database_name: str):
        """
        Update registered channels relations in database
        """
        update_response = self.registered_channel_service.update_registered_channel_relationships(registered_channel_id,
                                                                                                  registered_channel, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
