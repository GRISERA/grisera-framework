from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from measure.measure_model import MeasureIn, MeasureOut
from measure.measure_service import MeasureService

router = InferringRouter()


@cbv(router)
class MeasureRouter:
    """
    Class for routing measure based requests

    Attributes:
        measure_service (MeasureService): Service instance for measure
    """
    measure_service = MeasureService()

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
