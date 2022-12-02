from fastapi import Response, UploadFile, BackgroundTasks
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from typing import List
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

    @router.post("/model", tags=["models"], response_model=ModelOut)
    async def create_model(self,response: Response,background_tasks: BackgroundTasks, file: UploadFile = None):
        """
        Create ontology model based on uploaded file or base iri
        """
        if file is not None:
            create_response = self.model_service.save_model(file)
            background_tasks.add_task(os.remove, file.filename)
        else:
            create_response = self.model_service.create_base_model()
        if create_response.errors is not None:
            response.status_code = 422

            # add links from hateoas
        create_response.links = get_links(router)

        return create_response
        
    @router.get("/models/{id}", tags=["models"])
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

