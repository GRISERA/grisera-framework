from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dataset.dataset_model import DatasetIn, DatasetOut, DatasetsOut
from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from typing import Union
from services import Services

router = InferringRouter()


@cbv(router)
class DatasetRouter:
    """
    Class for routing dataset based requests

    Attributes:
        dataset_service (DatasetService): Service instance for datasets
    """

    def __init__(self):
        self.dataset_service = Services().dataset_service()

    @router.post("/datasets", tags=["datasets"], response_model=DatasetOut)
    async def create_dataset(self, response: Response, dataset_name_to_create: str):
        """
        Create dataset with given name
        """
        create_response = self.dataset_service.save_dataset(dataset_name_to_create)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/datasets/{database_name}", tags=["datasets"], response_model=Union[DatasetOut, NotFoundByIdModel])
    async def get_dataset(self, response: Response, dataset_name: str):
        """
        Get dataset by name
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
        Get all datasets by name
        """
        get_response = self.dataset_service.get_datasets()
        if get_response.errors is not None:
            response.status_code = 422

        get_response.links = get_links(router)

        return get_response

    @router.delete("/datasets/{database_name}", tags=["datasets"], response_model=Union[DatasetOut, NotFoundByIdModel])
    async def delete_dataset(self, response: Response, dataset_name: str):
        """
        Delete dataset by name
        """
        delete_response = self.dataset_service.delete_dataset(dataset_name)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response
