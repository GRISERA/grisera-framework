from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from measure.measure_model import MeasureIn, MeasuresOut, MeasureOut, MeasurePropertyIn, MeasureRelationIn
from measure.measure_service import MeasureService
from typing import Union
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class MeasureRouter:
    """
    Class for routing measure based requests

    Attributes:
        measure_service (MeasureService): Service instance for measures
    """
    def __init__(self):
        self.measure_service = Services().measure_service()

    @router.post("/measures", tags=["measures"], response_model=MeasureOut)
    async def create_measure(self, measure: MeasureIn, response: Response):
        """
        Create measure in database
        """

        create_response = self.measure_service.save_measure(measure)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/measures", tags=["measures"], response_model=MeasuresOut)
    async def get_measures(self, response: Response):
        """
        Get measures from database
        """

        get_response = self.measure_service.get_measures()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/measures/{measure_id}", tags=["measures"],
                response_model=Union[MeasureOut, NotFoundByIdModel])
    async def get_measure(self, measure_id: int, response: Response):
        """
        Get measure from database
        """

        get_response = self.measure_service.get_measure(measure_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/measures/{measure_id}", tags=["measures"],
                   response_model=Union[MeasureOut, NotFoundByIdModel])
    async def delete_measure(self, measure_id: int, response: Response):
        """
        Delete measure from database
        """
        get_response = self.measure_service.delete_measure(measure_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/measures/{measure_id}", tags=["measures"],
                response_model=Union[MeasureOut, NotFoundByIdModel])
    async def update_measure(self, measure_id: int, measure: MeasurePropertyIn,
                                       response: Response):
        """
        Update measure model in database
        """
        update_response = self.measure_service.update_measure(measure_id,
                                                                                  measure)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put("/measures/{measure_id}/relationships", tags=["measures"],
                response_model=Union[MeasureOut, NotFoundByIdModel])
    async def update_measure_relationships(self, measure_id: int,
                                                     measure: MeasureRelationIn, response: Response):
        """
        Update measure relations in database
        """
        update_response = self.measure_service.update_measure_relationships(measure_id,
                                                                                                measure)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
