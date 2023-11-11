from typing import Union

from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from scenario.scenario_model import ScenarioOut
from scenario.scenario_service import ScenarioService


class ScenarioServiceRelational(ScenarioService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.SCENARIO

    def get_scenario_by_activity_execution(self, activity_execution_id: Union[int, str], depth: int =0):
        scenario = self.rdb_api_service.get_scenario_by_activity_execution(self.table_name, activity_execution_id)
        if not scenario:
            return NotFoundByIdModel(id=activity_execution_id, errors={"Entity not found"})
        return ScenarioOut(**scenario)

    def delete_activity_execution(self, activity_execution_id: Union[int, str]):
        scenario = self.rdb_api_service.get_scenario_by_activity_execution(self.table_name, activity_execution_id)
        if not scenario:
            return NotFoundByIdModel(id=activity_execution_id, errors={"Entity not found"})
        import activity_execution.activity_execution_service_relational
        activity_execution_service_relational = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()
        self.rdb_api_service.delete_activity_execution_from_scenario(self.table_name, activity_execution_id, scenario["id"])
        return activity_execution_service_relational.get_activity_execution(activity_execution_id, 0)