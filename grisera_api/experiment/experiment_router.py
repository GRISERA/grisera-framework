from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from typing import Union
from experiment.experiment_model import ExperimentIn, ExperimentOut, ExperimentsOut
from experiment.experiment_service import ExperimentService
from models.not_found_model import NotFoundByIdModel
from services import Services

router = InferringRouter()


@cbv(router)
class ExperimentRouter:
    """
    Class for routing experiment based requests

    Attributes:
        experiment_service (ExperimentService): Service instance for experiments
    """
    def __init__(self):
        self.experiment_service = Services().experiment_service()

    @router.post("/experiments", tags=["experiments"], response_model=ExperimentOut)
    async def create_experiment(self, experiment: ExperimentIn, response: Response):
        """
        Create experiment in database
        """
        create_response = self.experiment_service.save_experiment(experiment)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/experiments/{experiment_id}", tags=["experiments"],
                response_model=Union[ExperimentOut, NotFoundByIdModel])
    async def get_experiment(self, experiment_id: int, response: Response):
        """
        Get experiment from database
        """

        get_response = self.experiment_service.get_experiment(experiment_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/experiments", tags=["experiments"], response_model=ExperimentsOut)
    async def get_experiments(self, response: Response):
        """
        Get experiments from database
        """

        get_response = self.experiment_service.get_experiments()

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/experiments/{experiment_id}", tags=["experiments"],
                   response_model=Union[ExperimentOut, NotFoundByIdModel])
    async def delete_experiment(self, experiment_id: Union[int, str], response: Response):
        """
        Delete experiment from database
        """
        get_response = self.experiment_service.delete_experiment(experiment_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/experiments/{experiment_id}", tags=["experiments"],
                response_model=Union[ExperimentOut, NotFoundByIdModel])
    async def update_experiment(self, experiment_id: int, experiment: ExperimentIn, response: Response):
        """
        Update experiment model in database
        """
        update_response = self.experiment_service.update_experiment(experiment_id, experiment)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
