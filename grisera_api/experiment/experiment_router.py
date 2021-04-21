from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from experiment.experiment_model import ExperimentIn, ExperimentOut
from experiment.experiment_service import ExperimentService

router = InferringRouter()


@cbv(router)
class ExperimentRouter:
    """
    Class for routing experiment based requests

    Attributes:
        experiment_service (ExperimentService): Service instance for experiments
    """
    experiment_service = ExperimentService()

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
