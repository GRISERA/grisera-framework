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
    async def get_measure_name(self, measure_name_id: Union[int, str], depth: int, response: Response):
        """
        Get measure name from database. Depth attribute specifies how many models will be traversed to create the
        response.
        """
        get_response = self.measure_name_service.get_measure_name(measure_name_id, depth)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/measure_names", tags=["measure names"], response_model=MeasureNamesOut)
    async def get_measure_names(self, response: Response):
        """
        Get measure names from database
        """

        get_response = self.measure_name_service.get_measure_names()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response
