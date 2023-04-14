from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dataset.dataset_model import DatasetIn, DatasetOut, DatasetsOut
from dataset.dataset_service import DatasetService
from hateoas import get_links
from typing import List
from property.property_model import PropertyIn
from models.not_found_model import NotFoundByIdModel
from typing import Union
from services import Services

router = InferringRouter()


@cbv(router)
class DatasetRouter:
    """
    Class for routing relationships based requests

    Attributes:
        relationship_service (RelationshipService): Service instance for relationships
    """
    def __init__(self):
        self.dataset_service = Services().dataset_service()

    @router.post("/dataset", tags=["datasets"], response_model=DatasetOut)
    async def create_dataset(self, response: Response, dataset_name_to_create: str):
        """
        Create directed and named dataset
        """
        create_response = self.dataset_service.save_dataset(dataset_name_to_create)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/datasets/{database_name}", tags=["datasets"],
                response_model=Union[DatasetsOut, NotFoundByIdModel])
    async def get_dataset(self, response: Response, dataset_name: str):
        """
        Get dataset from database
        """

        get_response = self.dataset_service.get_dataset(dataset_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/datasets", tags=["datasets"], response_model=DatasetsOut)
    async def get_datasets(self, response: Response):
        """
        Create directed and named dataset
        """
        #It don't have to be 'neo4j', any existing database will pass
        dataset_name = "neo4j"
        datasets = self.dataset_service.get_datasets(dataset_name)
        if datasets.errors is not None:
            response.status_code = 422

        datasets.links = get_links(router)

        return datasets

    @router.delete("/datasets/{database_name}", tags=["datasets"],
                   response_model=Union[DatasetsOut, NotFoundByIdModel])
    async def delete_dataset(self, response: Response, dataset_name: str):
        """
        Delete dataset from database
        """
        get_response = self.dataset_service.delete_dataset(dataset_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response