
from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from typing import List
from fastapi.responses import FileResponse
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

    @router.get("/models/{id}", tags=["models"], response_class=FileResponse)
    async def get_owl(self, model_id: int, response: Response):
        """
        Get OWL file from model with given id
        """
        get_response = self.model_service.get_owl_from_model(model_id)
        if get_response is None:
            response.status_code = 404
        # add links from hateoas
        # get_response.links = get_links(router)
        return FileResponse(get_response)

    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Ola

        return None
   
    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Stasiu

        return None
    
