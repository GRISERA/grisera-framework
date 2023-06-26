from fastapi import Response, UploadFile, File
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from fastapi.responses import FileResponse
from model.model_model import ModelOut
from instance.instance_model import MinimalInstanceModelIn
from instance.instance_service import InstanceService
import os


router = InferringRouter()


@cbv(router)
class InstanceRouter:
    """
    Class for routing model based requests
    Attributes:
        instance_service (InstanceService)
    """
    instance_service = InstanceService()

    @router.post("/models/{model_id}/classes/{class_name}/instances", tags=["instance"], response_model=None)
    async def add_instance(self, model_id: int, class_name: str,
                           model_in: MinimalInstanceModelIn, response: Response):
        """
                Create class instance in given model.

                Return 422 when model with given model_id don't exist
                or class with given class_name don't exist in model.
        """

        instance_out = self.instance_service.add_instance(model_id, class_name, model_in)
        if instance_out.errors is not None:
            response.status_code = 422

        instance_out.links = get_links(router)

        return instance_out

    @router.get("/models/{model_id}/classes/{class_name}/instances/{instance_label}", tags=["instance"],
                response_model=None)
    async def get_instance(self, model_id: int, class_name: str, instance_label: str, response: Response):

        """
                Return instance with a given label.

                Return 422 when a model with given model_id does not exist
                or class with given class_name does not exist in model or instance with given label does not exist.
        """
        instance_out = self.instance_service.get_instance(model_id, class_name, instance_label)
        if instance_out.errors is not None:
            response.status_code = 404

        instance_out.links = get_links(router)

        return instance_out

    @router.get("/models/{model_id}/classes/{class_name}/instances", tags=["instance"],
                response_model=None)
    async def get_instances(self, model_id: int, class_name: str, response: Response):
        """
            Return all instances of a given class in the model
            Return 404 when a model with given model_id does not exist
            or class with given class_name does not exist in model.
        """
        instances_out = self.instance_service.get_instances(model_id, class_name)
        if instances_out.errors is not None:
            response.status_code = 404

        instances_out.links = get_links(router)

        return instances_out

    @router.delete("/models/{model_id}/classes/{class_name}/instances/{instance_label}", tags=["instance"],
                response_model=None)
    async def delete_instance(self, model_id: int, class_name: str, instance_label: str, response: Response):

        """
                Delete instance with a given label.

                Return 404 when a model with given model_id does not exist
                or class with given class_name does not exist in model or instance with given label does not exist.
        """
        instance_out = self.instance_service.delete_instance(model_id, class_name, instance_label)
        if instance_out.errors is not None:
            response.status_code = 404

        instance_out.links = get_links(router)

        return instance_out

