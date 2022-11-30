from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from modality.modality_model import ModalityIn, ModalityOut, BasicModalityOut, ModalitiesOut
from modality.modality_service import ModalityService
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class ModalityRouter:
    """
    Class for routing modality based requests

    Attributes:
        modality_service (ModalityService): Service instance for modality
    """
    def __init__(self):
        self.modality_service = Services().modality_service()

    @router.get("/modalities/{modality_id}", tags=["modalities"],
                response_model=Union[ModalityOut, NotFoundByIdModel])
    async def get_modality(self, modality_id: int, response: Response):
        """
        Get modality from database
        """
        get_response = self.modality_service.get_modality(modality_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/modalities", tags=["modalities"], response_model=ModalitiesOut)
    async def get_modalities(self, response: Response):
        """
        Get modalities from database
        """

        get_response = self.modality_service.get_modalities()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
