from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from measure_name.measure_name_model import MeasureNameIn, MeasureNameOut, BasicMeasureNameOut, MeasureNamesOut
from measure_name.measure_name_service import MeasureNameService
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class MeasureNameRouter:
    """
    Class for routing measure name based requests

    Attributes:
        measure_name_service (MeasureNameService): Service instance for measure name
    """
    def __init__(self):
        self.measure_name_service = Services().measure_name_service()

    @router.get("/measure_names/{measure_name_id}", tags=["measure names"],
                response_model=Union[MeasureNameOut, NotFoundByIdModel])
    async def get_measure_name(self, measure_name_id: int, response: Response, database_name: str):
        """
        Get measure name from database
        """
        get_response = self.measure_name_service.get_measure_name(measure_name_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/measure_names", tags=["measure names"], response_model=MeasureNamesOut)
    async def get_measure_names(self, response: Response, database_name: str):
        """
        Get measure names from database
        """

        get_response = self.measure_name_service.get_measure_names(database_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
    @router.post("/measure_names", tags=["measure names"], response_model=MeasureNamesOut)
    async def create_measure_name(self, measure_name: MeasureNameIn, response: Response, database_name: str):
        """
        Create measure_name in database
        """
        create_response = self.measure_name_service.save_measure_name(measure_name, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.delete("/measure_names/{measure_name_id}", tags=["measure names"],
                   response_model=Union[MeasureNameOut, NotFoundByIdModel])
    async def delete_measure_name(self, measure_name_id: int, response: Response, database_name: str):
        """
        Delete measure_name from database
        """
        get_response = self.measure_name_service.delete_measure_name(measure_name_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/measure_names/{measure_name_id}", tags=["measure names"],
                response_model=Union[MeasureNameOut, NotFoundByIdModel])
    async def update_measure_name(self, measure_name_id: int, measure_name: MeasureNameIn, response: Response, database_name: str):
        """
        Update measure_name model in database
        """
        update_response = self.measure_name_service.update_measure_name(measure_name_id, measure_name, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
