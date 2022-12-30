from fastapi import Response, UploadFile, BackgroundTasks, File
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from fastapi.responses import FileResponse
from model.model_model import ModelOut
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
        Create ontology model based on uploaded file
        """

        create_response = self.model_service.save_model(file)

        if create_response.errors is not None:
            print(create_response.errors)
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/model_basic", tags=["model"], response_model=ModelOut)
    async def create_base_model(self, response: Response):
        """
        Create base ontology model
        """

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
            return FileResponse(get_response, media_type="application/xml")
