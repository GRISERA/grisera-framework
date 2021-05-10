from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from scenario.scenario_model import ScenarioIn, ScenarioOut
from scenario.scenario_service import ScenarioService

router = InferringRouter()


@cbv(router)
class ScenarioRouter:
    """
    Class for routing scenario based requests

    Attributes:
        scenario_service (ScenarioService): Service instance for scenarios
    """
    scenario_service = ScenarioService()

    @router.post("/scenarios", tags=["scenarios"], response_model=ScenarioOut)
    async def create_scenario(self, scenario: ScenarioIn, response: Response):
        """
        Create scenario in database
        """
        create_response = self.scenario_service.save_scenario(scenario)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
