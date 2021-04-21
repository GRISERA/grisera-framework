from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from author.author_model import AuthorIn, AuthorOut
from author.author_service import AuthorService

router = InferringRouter()


@cbv(router)
class AuthorRouter:
    """
    Class for routing author based requests

    Attributes:
        author_service (AuthorService): Service instance for authors
    """
    author_service = AuthorService()

    @router.post("/authors", tags=["authors"], response_model=AuthorOut)
    async def create_author(self, author: AuthorIn, response: Response):
        """
        Create author in database
        """
        create_response = self.author_service.save_author(author)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
