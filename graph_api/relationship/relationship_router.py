from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from relationship.relationship_model import RelationshipIn, RelationshipOut
from relationship.relationship_service import RelationshipService
from hateoas import get_links
from typing import List
from property.property_model import PropertyIn

router = InferringRouter()


@cbv(router)
class RelationshipRouter:
    """
    Class for routing relationships based requests

    Attributes:
        relationship_service (RelationshipService): Service instance for relationships
    """

    relationship_service = RelationshipService()

    @router.post("/relationships", tags=["relationships"], response_model=RelationshipOut)
    async def create_relationship(self, relationship: RelationshipIn, response: Response, database_name: str):
        """
        Create directed and named relationship
        """
        create_response = self.relationship_service.save_relationship(relationship, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/relationships/{id}/properties", tags=["relationships"], response_model=RelationshipOut)
    async def create_relationship_properties(self, id: int, properties: List[PropertyIn], response: Response, database_name: str):
        """
        Create properties for relationship with given id
        """
        create_response = self.relationship_service.save_properties(id, properties, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.delete("/relationships/{id}", tags=["relationships"], response_model=RelationshipOut)
    async def delete_relationship(self, id: int, response: Response, database_name: str):
        """
        Delete relationship by id
        """
        delete_response = self.relationship_service.delete_relationship(id, database_name)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response
