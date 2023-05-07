from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from role.role_service import RoleService
from role.role_model import RoleModelIn

router = InferringRouter()


@cbv(router)
class RoleRouter:
    """
        Class for routing role based requests
        Attributes:
            role_service (RoleService): Service instance for roles

    """
    role_service = RoleService()

    @router.post("/models/{model_id}/roles", tags=["role"], response_model=None)
    async def add_role(self, model_id: int, model_in: RoleModelIn, response: Response):
        """
                Create an instance of a property in the given model
                Return 404 when model with the given id does not exist
        """
        role_out = self.role_service.add_role(model_id, model_in)
        if role_out.errors is not None:
            response.status_code = 404

        role_out.links = get_links(router)

        return role_out

    @router.delete("/models/{model_id}/instances/{instance_name}/roles", tags=["role"], response_model=None)
    async def delete_roles(self, model_id: int, instance_name: str, response: Response):
        """
                Delete all relationships of the given individual
                Return 404 when model or instance not found
        """
        role_out = self.role_service.delete_roles(model_id, instance_name)
        
        if role_out.errors is not None:
            response.status_code = 404

        role_out.links = get_links(router)

        return role_out
