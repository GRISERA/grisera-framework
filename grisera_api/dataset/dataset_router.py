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
import time

from modality.modality_model import ModalityIn
from modality.modality_model import Modality as modality_types
from life_activity.life_activity_model import LifeActivityIn
from life_activity.life_activity_model import LifeActivity as life_activity_types
from channel.channel_model import ChannelIn
from channel.channel_model import Type as channel_types
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
        self.channel_service = Services().channel_service()
        self.modality_service = Services().modality_service()
        self.life_activity_service = Services().life_activity_service()

    @router.post("/datasets", tags=["datasets"], response_model=DatasetOut)
    async def create_dataset(self, response: Response, dataset_name_to_create: str):
        """
        Create directed and named dataset
        """
        create_dataset_response = self.dataset_service.save_dataset(dataset_name_to_create)
        if create_dataset_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_dataset_response.links = get_links(router)

        # wait for the dataset to be created
        time.sleep(0.5)

        # create channels nodes for the dataset
        for channel_type in channel_types:
            create_channel_response = self.channel_service.save_channel(ChannelIn(type=channel_type.value), dataset_name_to_create)

        # create modalities nodes for the dataset
        for modality_type in modality_types:
            create_modality_response = self.modality_service.save_modality(ModalityIn(modality=modality_type.value), dataset_name_to_create)

        # create life activities nodes for the dataset
        for life_activity_type in life_activity_types:
            create_life_activity_response = self.life_activity_service.save_life_activity(LifeActivityIn(life_activity=life_activity_type.value), dataset_name_to_create)

        return create_dataset_response

    @router.get("/datasets/{database_name}", tags=["datasets"],
                response_model=Union[DatasetOut, NotFoundByIdModel])
    async def get_dataset(self, response: Response, dataset_name: str):
        """
        Get dataset from database by name
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
                   response_model=Union[DatasetOut, NotFoundByIdModel])
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