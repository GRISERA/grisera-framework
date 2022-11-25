
from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from model.model_service import ModelService
from hateoas import get_links
from typing import List
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

    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Pawel

        return None

    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Ola

        return None
   
    @router.post("/models", tags=["models"], response_model=None)
    async def create_model(self, wymyslsobieparametrjakiswejsciowybedziedobrze: int, response: Response):
        #TODO Stasiu

        return None
    
