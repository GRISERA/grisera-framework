from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dataset.dataset_model import DatasetIn, DatasetOut, DatasetsOut
from dataset.dataset_service import DatasetService
from hateoas import get_links
import time

router = InferringRouter()


@cbv(router)
class DatasetRouter:
    """
    Class for routing datasets based requests

    Attributes:
        dataset_service (DatasetService): Service instance for datasets
    """

    dataset_service = DatasetService()

    @router.post("/datasets", tags=["name_by_user"], response_model=DatasetOut)
    async def create_dataset(self, dataset: DatasetIn, response: Response):
        """
        Create dataset with given name
        """
        create_database_response = self.dataset_service.create_dataset(dataset.name_by_user)
        if create_database_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_database_response.links = get_links(router)

        time.sleep(1)  # wait for the db to be created

        create_alias_response = self.dataset_service.create_alias_for_database_with_name(
            create_database_response.name_hash,
            create_database_response.name_by_user)

        if create_alias_response.errors is not None:
            response.status_code = 422

        return create_alias_response

    @router.get("/datasets/{dataset_name}", tags=["response"], response_model=DatasetOut)
    async def get_dataset(self, dataset_name: str, response: Response):
        """
        Get dataset by name
        """
        dataset = self.dataset_service.get_dataset(dataset_name)
        if dataset.errors is not None:
            response.status_code = 422

        dataset.links = get_links(router)

        return dataset

    @router.get("/datasets", tags=["datasets"], response_model=DatasetsOut)
    async def get_datasets(self, response: Response):
        """
        Get all datasets by name
        """
        datasets = self.dataset_service.get_datasets()
        if datasets.errors is not None:
            response.status_code = 422

        datasets.links = get_links(router)

        return datasets

    @router.delete("/datasets/{dataset_name}", tags=["datasets"], response_model=DatasetOut)
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
