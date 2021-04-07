from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from relationship.relationship_model import RelationshipIn, RelationshipOut
from relationship.relationship_service import RelationshipService
from hateoas import get_links

router = InferringRouter()


@cbv(router)
class RelationshipRouter:
    """
    Class for routing relationships based requests

    Attributes:
        relationship_service (RelationshipService): Service instance for nodes
    """

    relationship_service = RelationshipService()

    @router.post("/relationships", tags=["relationships"], response_model=RelationshipOut)
    async def create_relationship(self, relationship: RelationshipIn, response: Response):
        """
        Create directed and named relationship
        """
        create_response = self.relationship_service.save_relationship(relationship)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
