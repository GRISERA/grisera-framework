from typing import Union, Optional

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request

from hateoas import get_links
from signal_series.signal_series_model import (
    SignalSeriesIn,
    SignalSeriesNodesOut,
    SignalSeriesOut,
    SignalSeriesPropertyIn,
    SignalSeriesRelationIn,
    SignalSeriesTransformationIn,
    SignalSeriesMultidimensionalOut
)
from time_series.time_series_service import TimeSeriesService
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class TimeSeriesRouter:
    """
    Class for routing time series based requests

    Attributes:
        time_series_service (TimeSeriesService): Service instance for time series
    """

    def __init__(self):
        self.time_series_service = Services().time_series_service()

    @router.post("/time_series", tags=["time series"], response_model=SignalSeriesOut)
    async def create_time_series(self, time_series: SignalSeriesIn, response: Response):
        """
        Create time series in database

        Signal_Values:
        - should be provided in ascending order of (start) timestamp
        - timestamps within one time series should be unique (for Timestamp type) and disjoint (for Epoch type)
        """

        create_response = self.time_series_service.save_signal_series(
            time_series)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/time_series/transformation", tags=["time series"],
                 response_model=Union[SignalSeriesOut, NotFoundByIdModel])
    async def transform_signal_series(self, time_series_transformation: SignalSeriesTransformationIn, response: Response):
        """
        Create new transformed time series in database

        Each transformation uses a different set of parameters.

        Supported transformation names and parameters:
        - resample_nearest:
            - period (required) - difference between output timestamps
            - start_timestamp - first output timestamp (default 0)
            - end_timestamp - last output timestamp will be less than end_timestamp (default last input end timestamp + period)
        - quadrants:
            - origin_x - X value of the center point of coordinate system (default 0)
            - origin_y - Y value of the center point of coordinate system (default 0)

        To read about the implementation details go to SignalSeriesTransformation docstring documentation.
        """

        create_response = self.time_series_service.transform_signal_series(
            time_series_transformation)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/time_series", tags=["time series"], response_model=SignalSeriesNodesOut)
    async def get_signal_series_nodes(self, response: Response, request: Request,
                                      entityname_property_name: Optional[str] = None,
                                      experiment_id: Optional[int] = None,
                                      participant_id: Optional[int] = None,
                                      participant_date_of_birth: Optional[str] = None,
                                      participant_sex: Optional[str] = None,
                                      participant_name: Optional[str] = None,
                                      participantstate_age: Optional[str] = None,
                                      recording_id: Optional[int] = None,
                                      recording_source: Optional[str] = None):
        """
        Get time series from database.

        The list of available parameters is not limited to the given below.

        This request allows filtering time series by id or any property from entities connected to time series.
        The format of this generic GET filter parameter is: `entityname_property_name`.

        Supported entity names:
        - observableinformation
        - recording
        - participation
        - participantstate
        - participant
        - activityexecution
        - activity
        - experiment
        - registeredchannel
        - channel
        - registereddata
        """

        get_response = self.time_series_service.get_signal_series_nodes(
            request.query_params)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/time_series/{time_series_id}",
        tags=["time series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def get_signal_series(
        self, time_series_id: Union[int, str], depth: int, response: Response,
        signal_min_value: Optional[int] = None,
        signal_max_value: Optional[int] = None
    ):
        """
        Get time series by id from database with Signal_Values. Depth attribute specifies how many models will be traversed to create the
        response.

        Signal_Values will be filtered using minimum and maximum value if present.
        """

        get_response = self.time_series_service.get_signal_series(
            time_series_id, depth, signal_min_value, signal_max_value)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/time_series/multidimensional/{time_series_ids}", tags=["time series"],
                response_model=Union[SignalSeriesMultidimensionalOut, NotFoundByIdModel])
    async def get_signal_series_multidimensional(self, time_series_ids: str, response: Response):
        """
        Get multidimensional time series by ids from database with Signal_Values.

        Time series ids is comma separated string.
        """
        try:
            ids = [int(time_series_id.strip())
                   for time_series_id in time_series_ids.split(",")]
        except ValueError:
            response.status_code = 422
            return SignalSeriesMultidimensionalOut(errors="Ids must be integers")

        get_response = self.time_series_service.get_signal_series_multidimensional(
            ids)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/time_series/{time_series_id}",
        tags=["time series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def delete_signal_series(
        self, time_series_id: Union[int, str], response: Response
    ):
        """
        Delete time series by id from database with all Signal_Values.
        """
        get_response = self.time_series_service.delete_signal_series(
            time_series_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/time_series/{time_series_id}",
        tags=["time series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def update_signal_series(
        self,
        time_series_id: Union[int, str],
        time_series: SignalSeriesPropertyIn,
        response: Response,
    ):
        """
        Update time series model in database
        """
        update_response = self.time_series_service.update_signal_series(
            time_series_id, time_series
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/time_series/{time_series_id}/relationships",
        tags=["time series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def update_signal_series_relationships(
        self,
        time_series_id: Union[int, str],
        time_series: SignalSeriesRelationIn,
        response: Response,
    ):
        """
        Update time series relations in database
        """
        update_response = self.time_series_service.update_signal_series_relationships(
            time_series_id, time_series
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
