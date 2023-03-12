from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from role.role_service import RoleService
from role.role_model import ObjectPropertyRoleModelIn, DataTypePropertyRoleModelIn

router = InferringRouter()


@cbv(router)
class RoleRouter:
    """
        Class for routing role based requests
        Attributes:
            role_service (RoleService): Service instance for roles

    """
    role_service = RoleService()

    @router.post("/models/{model_id}/roles/object", tags=["role"], response_model=None)
    async def add_object_property_role(self, model_id: int, model_in: ObjectPropertyRoleModelIn, response: Response):
        """
                Create an instance of an object property in the given model
                Return 404 when model with the given id does not exist
        """
        role_out = self.role_service.add_object_property_role(model_id, model_in)
        if role_out.errors is not None:
            response.status_code = 404

        role_out.links = get_links(router)

        return role_out

    @router.post("/models/{model_id}/roles/datatype", tags=["role"], response_model=None)
    async def add_datatype_property_role(self, model_id: int, model_in: DataTypePropertyRoleModelIn,
                                         response: Response):
        """
                Create an instance of an DataType property in the given model
                Return 404 when model with the given id does not exist
        """
        role_out = self.role_service.add_datatype_property_role(model_id, model_in)
        if role_out.errors is not None:
            response.status_code = 404

        role_out.links = get_links(router)

        return role_out
