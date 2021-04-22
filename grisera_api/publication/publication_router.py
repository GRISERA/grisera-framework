from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from publication.publication_model import PublicationIn, PublicationOut
from publication.publication_service import PublicationService

router = InferringRouter()


@cbv(router)
class PublicationRouter:
    """
    Class for routing publication based requests

    Attributes:
        publication_service (PublicationService): Service instance for publications
    """
    publication_service = PublicationService()

    @router.post("/publications", tags=["publications"], response_model=PublicationOut)
    async def create_publication(self, publication: PublicationIn, response: Response):
        """
        Create publication in database
        """
        create_response = self.publication_service.save_publication(publication)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
