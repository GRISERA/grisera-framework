from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from modality.modality_model import ModalityIn, ModalityOut
from modality.modality_service import ModalityService

router = InferringRouter()


@cbv(router)
class ModalityRouter:
    """
    Class for routing modality based requests

    Attributes:
        modality_service (ModalityService): Service instance for modality
    """
    modality_service = ModalityService()

    @router.post("/modality", tags=["modality"], response_model=ModalityOut)
    async def create_modality(self, modality: ModalityIn, response: Response):
        """
        Create modality in database
        """
        create_response = self.modality_service.save_modality(modality)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
