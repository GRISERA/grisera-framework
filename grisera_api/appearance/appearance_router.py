from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from appearance.appearance_model import AppearanceOcclusionIn, AppearanceOcclusionOut, \
    AppearanceSomatotypeIn, AppearanceSomatotypeOut
from appearance.appearance_service import AppearanceService

router = InferringRouter()


@cbv(router)
class AppearanceRouter:
    """
    Class for routing appearance based requests

    Attributes:
        appearance_service (AppearanceService): Service instance for appearance
    """
    appearance_service = AppearanceService()

    @router.post("/appearance/occlusion_model", tags=["appearance"], response_model=AppearanceOcclusionOut)
    async def create_appearance_occlusion(self, appearance: AppearanceOcclusionIn, response: Response):
        """
        Create appearance occlusion model in database
        """

        create_response = self.appearance_service.save_appearance_occlusion(appearance)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/appearance/somatotype_model", tags=["appearance"], response_model=AppearanceSomatotypeOut)
    async def create_appearance_somatotype(self, appearance: AppearanceSomatotypeIn, response: Response):
        """
        Create appearance somatotype model in database
        """

        create_response = self.appearance_service.save_appearance_somatotype(appearance)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
