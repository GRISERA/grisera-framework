from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from registered_data.registered_data_model import RegisteredDataIn, RegisteredDataOut, BasicRegisteredDataOut, \
    RegisteredDataNodesOut
from registered_data.registered_data_service import RegisteredDataService
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class RegisteredDataRouter:
    """
    Class for routing registered data based requests

    Attributes:
        registered_data_service (RegisteredDataService): Service instance for registered data
    """

    def __init__(self):
        self.registered_data_service = Services().registered_data_service()

    @router.post("/registered_data", tags=["registered data"], response_model=RegisteredDataOut)
    async def create_registered_data(self, registered_data: RegisteredDataIn, response: Response, database_name: str):
        """
        Create registered data in database
        """
        create_response = self.registered_data_service.save_registered_data(registered_data, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/registered_data/{registered_data_id}", tags=["registered data"],
                response_model=Union[RegisteredDataOut, NotFoundByIdModel])
    async def get_registered_data(self, registered_data_id: int, response: Response, database_name: str):
        """
        Get registered data from database
        """

        get_response = self.registered_data_service.get_registered_data(registered_data_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/registered_data", tags=["registered data"], response_model=RegisteredDataNodesOut)
    async def get_registered_data_nodes(self, response: Response, database_name: str):
        """
        Get registered data from database
        """

        get_response = self.registered_data_service.get_registered_data_nodes(database_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/registered_data/{registered_data_id}", tags=["registered data"],
                   response_model=Union[RegisteredDataOut, NotFoundByIdModel])
    async def delete_registered_data(self, registered_data_id: int, response: Response, database_name: str):
        """
        Delete registered data from database
        """
        get_response = self.registered_data_service.delete_registered_data(registered_data_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/registered_data/{registered_data_id}", tags=["registered data"],
                response_model=Union[RegisteredDataOut, NotFoundByIdModel])
    async def update_registered_data(self, registered_data_id: int, registered_data: RegisteredDataIn,
                                     response: Response, database_name: str):
        """
        Update registered data model in database
        """
        update_response = self.registered_data_service.update_registered_data(registered_data_id, registered_data, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
