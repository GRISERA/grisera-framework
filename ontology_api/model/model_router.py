from fastapi import Response, UploadFile, BackgroundTasks, File
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from fastapi.responses import FileResponse
from model.model_model import ModelOut
from instance.instance_model import MinimalInstanceModelIn
import os

router = InferringRouter()


@cbv(router)
class ModelRouter:
    """
    Class for routing model based requests
    Attributes:
        model_service (ModelService): Service instance for models
    """
    model_service = ModelService()

    @router.post("/model", tags=["model"], response_model=ModelOut)
    async def create_model(self, response: Response, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
        # Problem with using UploadFile with Pydantic model:
        # "Value not declarable with JSON Schema".
        # Quick fix based on https://github.com/tiangolo/fastapi/issues/657
        """
        Create ontology model based on uploaded file or base iri
        """
        if isinstance(file, UploadFile):
            create_response = self.model_service.save_model(file)
            background_tasks.add_task(os.remove, file.filename)
        else:
            create_response = self.model_service.create_base_model()
        if create_response.errors is not None:
            response.status_code = 422

            # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/model/{id}", tags=["model"])
    async def get_owl(self, id: int, response: Response, background_tasks: BackgroundTasks):
        """
        Get OWL file from model with given id
        """
        get_response = self.model_service.get_owl_from_model(id)
        if get_response is None:
            response.status_code = 404
            return {"error": "File not found!"}
        else:
            background_tasks.add_task(os.remove, get_response)
            return FileResponse(get_response, media_type="application/xml")

    @router.post("/models/{model_id}/classes/{class_name}/instances", tags=["models"], response_model=None)
    async def add_instance(self, model_id: int, class_name: str,
                           model_in: MinimalInstanceModelIn, response: Response):
        """
                Create class instance in given model.

                Return 422 when model with given model_id don't exist
                or class with given class_name don't exist in model.
        """

        errors = self.model_service.add_instance(model_id, class_name, model_in)

        if errors is not None:
            response.status_code = 422
            return errors

        return None
