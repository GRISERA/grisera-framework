from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from time_series.time_series_model import TimeSeriesIn, TimeSeriesOut
from time_series.time_series_service import TimeSeriesService

router = InferringRouter()


@cbv(router)
class TimeSeriesRouter:
    """
    Class for routing time_series based requests

    Attributes:
        time_series_service (TimeSeriesService): Service instance for time_series
    """
    time_series_service = TimeSeriesService()

    @router.post("/time_series", tags=["time series"], response_model=TimeSeriesOut)
    async def create_time_series(self, time_series: TimeSeriesIn, response: Response):
        """
        Create time_series in database
        """
        create_response = self.time_series_service.save_time_series(time_series)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
