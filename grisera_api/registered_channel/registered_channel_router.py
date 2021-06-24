from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from registered_channel.registered_channel_model import RegisteredChannelIn, RegisteredChannelOut
from registered_channel.registered_channel_service import RegisteredChannelService

router = InferringRouter()


@cbv(router)
class RegisteredChannelRouter:
    """
    Class for routing registered channel based requests

    Attributes:
        activity_service (ActivityService): Service instance for registered channel
    """
    registered_channel_service = RegisteredChannelService()

    @router.post("/registered_channels", tags=["registered channels"], response_model=RegisteredChannelOut)
    async def create_registered_channel(self, registered_channel: RegisteredChannelIn, response: Response):
        """
        Create registered channel in database
        """
        create_response = self.registered_channel_service.save_registered_channel(registered_channel)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
