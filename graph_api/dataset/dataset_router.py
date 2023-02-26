from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dataset.dataset_model import DatasetIn, DatasetOut, DatasetsOut
from dataset.dataset_service import DatasetService
from hateoas import get_links
from typing import List
from property.property_model import PropertyIn

router = InferringRouter()


@cbv(router)
class DatasetRouter:
    """
    Class for routing relationships based requests

    Attributes:
        relationship_service (RelationshipService): Service instance for relationships
    """

    dataset_service = DatasetService()

    @router.post("/dataset", tags=["datasets"], response_model=DatasetOut)
    async def create_dataset(self, dataset: DatasetIn, response: Response, database_name_to_create: str, database_name: str):
        """
        Create directed and named dataset
        """
        create_response = self.dataset_service.create_dataset(dataset, database_name_to_create, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/datasets", tags=["datasets"], response_model=DatasetsOut)
    async def get_datasets(self, response: Response, database_name: str):
        """
        Create directed and named dataset
        """
        datasets = self.dataset_service.get_datasets(database_name)
        if datasets.errors is not None:
            response.status_code = 422

        datasets.links = get_links(router)

        return datasets