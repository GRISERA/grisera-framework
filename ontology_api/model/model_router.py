from fastapi import Response, File, UploadFile, BackgroundTasks
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from typing import List
from fastapi.responses import FileResponse, JSONResponse
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

    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Kuchta

        return None
        
    @router.post("/upload")
    async def upload_file(self, file: UploadFile):
        with open(file.filename, 'wb') as image:
            content = await file.read()
            image.write(content)
            image.close()
        return JSONResponse(content={"filename": file.filename},status_code=200)

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

    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Ola

        return None
   
    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Stasiu

        return None
