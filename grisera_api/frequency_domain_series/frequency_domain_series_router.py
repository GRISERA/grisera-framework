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
from frequency_domain_series.frequency_domain_series_service import FrequencyDomainSeriesService
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class FrequencyDomainSeriesRouter:
    """
    Class for routing frequency domain series based requests

    Attributes:
        frequency_domain_series_service (FrequencyDomainSeriesService): Service instance for frequency domain series
    """

    def __init__(self):
        self.frequency_domain_series_service = Services().frequency_domain_series_service()

    @router.post("/frequency_domain_series", tags=["frequency domain series"], response_model=SignalSeriesOut)
    async def create_frequency_domain_series(self, frequency_domain_series: SignalSeriesIn, response: Response):
        """
        Create frequency domain series in database

        Signal_Values:
        - should be provided in ascending order of (start) frequencystamp
        - frequencystamps within one frequency domain series should be unique (for Timestamp type)
        """

        create_response = self.frequency_domain_series_service.save_signal_series(frequency_domain_series)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.post("/frequency_domain_series/transformation", tags=["frequency domain series"],
                 response_model=Union[SignalSeriesOut, NotFoundByIdModel])
    async def transform_signal_series(self, frequency_domain_series_transformation: SignalSeriesTransformationIn, response: Response):
        """
        Create new transformed frequency domain series in database

        Each transformation uses a different set of parameters.

        Supported transformation names and parameters:
        - fouriers

        To read about the implementation details go to FrequencyDomainSeriesTransformation docstring documentation.
        """

        create_response = self.frequency_domain_series_service.transform_signal_series(frequency_domain_series_transformation)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/frequency_domain_series", tags=["frequency domain series"], response_model=SignalSeriesNodesOut)
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
        Get frequency domain series from database.

        The list of available parameters is not limited to the given below.

        This request allows filtering frequency domain series by id or any property from entities connected to frequency domain series.
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

        get_response = self.frequency_domain_series_service.get_signal_series_nodes(request.query_params)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get(
        "/frequency_domain_series/{frequency_domain_series_id}",
        tags=["frequency domain series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def get_signal_series(
        self, frequency_domain_series_id: Union[int, str], depth: int, response: Response,
        signal_min_value: Optional[int] = None,
        signal_max_value: Optional[int] = None
    ):
        """
        Get frequency domain series by id from database with Signal_Values. Depth attribute specifies how many models will be traversed to create the
        response.

        Signal_Values will be filtered using minimum and maximum value if present.
        """

        get_response = self.frequency_domain_series_service.get_signal_series(frequency_domain_series_id, depth, signal_min_value, signal_max_value)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/frequency_domain_series/multidimensional/{frequency_domain_series_ids}", tags=["frequency domain series"],
                response_model=Union[SignalSeriesMultidimensionalOut, NotFoundByIdModel])
    async def get_signal_series_multidimensional(self, frequency_domain_series_ids: str, response: Response):
        """
        Get multidimensional frequency domain series by ids from database with Signal_Values.

        Time series ids is comma separated string.
        """
        try:
            ids = [int(frequency_domain_series_id.strip()) for frequency_domain_series_id in frequency_domain_series_ids.split(",")]
        except ValueError:
            response.status_code = 422
            return SignalSeriesMultidimensionalOut(errors="Ids must be integers")

        get_response = self.frequency_domain_series_service.get_signal_series_multidimensional(ids)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete(
        "/frequency_domain_series/{frequency_domain_series_id}",
        tags=["frequency domain series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def delete_signal_series(
        self, frequency_domain_series_id: Union[int, str], response: Response
    ):
        """
        Delete frequency domain series by id from database with all Signal_Values.
        """
        get_response = self.frequency_domain_series_service.delete_signal_series(frequency_domain_series_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put(
        "/frequency_domain_series/{frequency_domain_series_id}",
        tags=["frequency domain series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def update_signal_series(
        self,
        frequency_domain_series_id: Union[int, str],
        frequency_domain_series: SignalSeriesPropertyIn,
        response: Response,
    ):
        """
        Update frequency domain series model in database
        """
        update_response = self.frequency_domain_series_service.update_signal_series(
            frequency_domain_series_id, frequency_domain_series
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put(
        "/frequency_domain_series/{frequency_domain_series_id}/relationships",
        tags=["frequency domain series"],
        response_model=Union[SignalSeriesOut, NotFoundByIdModel],
    )
    async def update_signal_series_relationships(
        self,
        frequency_domain_series_id: Union[int, str],
        frequency_domain_series: SignalSeriesRelationIn,
        response: Response,
    ):
        """
        Update frequency domain series relations in database
        """
        update_response = self.frequency_domain_series_service.update_signal_series_relationships(
            frequency_domain_series_id, frequency_domain_series
        )
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
