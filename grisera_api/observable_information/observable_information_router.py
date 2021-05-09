from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut
from observable_information.observable_information_service import ObservableInformationService

router = InferringRouter()


@cbv(router)
class ObservableInformationRouter:
    """
    Class for routing observable information based requests

    Attributes:
        observable_information_service (ObservableInformationService): Service instance for observable information
    """
    observable_information_service = ObservableInformationService()

    @router.post("/observable_information", tags=["observable information"], response_model=ObservableInformationOut)
    async def create_observable_information(self, observable_information: ObservableInformationIn, response: Response):
        """
        Create observable information in database
        """
        create_response = self.observable_information_service.save_observable_information(observable_information)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
