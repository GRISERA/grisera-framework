from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from signal_node.signal_model import SignalIn, SignalOut
from signal_node.signal_service import SignalService

router = InferringRouter()


@cbv(router)
class SignalRouter:
    """
    Class for routing signal based requests

    Attributes:
        signal_service (SignalService): Service instance for signals
    """
    signal_service = SignalService()

    @router.post("/signals", tags=["signals"], response_model=SignalOut)
    async def create_signal(self, signal: SignalIn, response: Response):
        """
        Create signal in database
        """
        create_response = self.signal_service.save_signal(signal)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
