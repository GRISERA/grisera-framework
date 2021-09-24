from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from registered_data.registered_data_model import RegisteredDataIn, RegisteredDataOut
from registered_data.registered_data_service import RegisteredDataService

router = InferringRouter()


@cbv(router)
class RegisteredDataRouter:
    """
    Class for routing registered data based requests

    Attributes:
        registered_data_service (RegisteredDataService): Service instance for registered data
    """
    registered_data_service = RegisteredDataService()

    @router.post("/registered_data", tags=["registered data"], response_model=RegisteredDataOut)
    async def create_registered_data(self, registered_data: RegisteredDataIn, response: Response):
        """
        Create registered data in database
        """
        create_response = self.registered_data_service.save_registered_data(registered_data)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
