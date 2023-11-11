from typing import Union
from activity_execution.activity_execution_model import ActivityExecutionIn
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from scenario.scenario_model import ScenarioOut, ScenarioIn, OrderChangeIn, OrderChangeOut
from scenario.scenario_service import ScenarioService


class ScenarioServiceRelational(ScenarioService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.SCENARIO

    def save_scenario(self, scenario: ScenarioIn):
        scenario_dict = scenario.dict()
        activity_execution_ids = []

        import activity_execution.activity_execution_service_relational
        activity_execution_service_relational = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()
        import experiment.experiment_service_relational
        experiment_service_relational = experiment.experiment_service_relational.ExperimentServiceRelational()


        experiment = experiment_service_relational.get_experiment(scenario_dict["experiment_id"])
        if not experiment:
            return NotFoundByIdModel(id=scenario_dict["experiment_id"], errors={"Entity not found"})

        for activity_execution in scenario_dict["activity_executions"]:
            activity_execution_ids.append(activity_execution["id"])
            activity_execution_service_relational.save_activity_execution(activity_execution)
        scenario_dict["activity_executions"] = activity_execution_ids
        result = self.rdb_api_service.post(self.table_name, scenario_dict)
        if result["errors"] is not None:
            return ScenarioOut(errors=result["errors"])
        result["records"]["activity_executions"] = scenario_dict["activity_executions"]
        return ScenarioOut(**result["records"])

    def add_activity_execution(self, previous_id: Union[int, str], activity_execution: ActivityExecutionIn):
        scenario = self.get_scenario_by_activity_execution_with_id_list(previous_id)
        if type(scenario) is NotFoundByIdModel:
            return scenario
        import activity_execution.activity_execution_service_relational as activity_execution_service
        activity_execution_service_relational = activity_execution_service.ActivityExecutionServiceRelational()
        save_result = activity_execution_service_relational.save_activity_execution(activity_execution)

        if save_result.errors is not None:
            return save_result

        index_of_previous_id = scenario["activity_executions"].index(previous_id)
        scenario["activity_executions"].insert(index_of_previous_id + 1, save_result.id)
        self.rdb_api_service.put(self.table_name, scenario["id"], scenario)
        return save_result

    def get_scenario_by_activity_execution_with_id_list(self, activity_execution_id: Union[int, str], depth: int =0):
        scenario = self.rdb_api_service.get_scenario_by_activity_execution(self.table_name, activity_execution_id)
        if not scenario:
            return NotFoundByIdModel(id=activity_execution_id, errors={"Entity not found"})
        return scenario

    def delete_activity_execution(self, activity_execution_id: Union[int, str]):
        scenario = self.rdb_api_service.get_scenario_by_activity_execution(self.table_name, activity_execution_id)
        if not scenario:
            return NotFoundByIdModel(id=activity_execution_id, errors={"Entity not found"})

        import activity_execution.activity_execution_service_relational
        activity_execution_service_relational = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()

        self.rdb_api_service.delete_activity_execution_from_scenario(self.table_name, activity_execution_id, scenario["id"])
        return activity_execution_service_relational.get_activity_execution(activity_execution_id, 0)

    def get_scenario(self, element_id: Union[int, str], depth: int = 0):
        import experiment.experiment_service_relational
        experiment_service_relational = experiment.experiment_service_relational.ExperimentServiceRelational()
        experiment = experiment_service_relational.get_experiment(element_id)
        if type(experiment) is NotFoundByIdModel:
            return self.get_scenario_by_activity_execution(element_id,depth)
        return self.get_scenario_by_experiment(experiment.id, depth)


    def get_scenario_by_activity_execution(self, activity_execution_id: Union[int, str], depth: int = 0):
        scenario = self.get_scenario_by_activity_execution_with_id_list(activity_execution_id)
        if type(scenario) is NotFoundByIdModel:
            return scenario
        import activity_execution.activity_execution_service_relational
        activity_execution_service_relational = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()
        activity_execution_list = []
        for activity_execution_id in scenario["activity_executions"]:
            activity_execution = activity_execution_service_relational.get_activity_execution(activity_execution_id, depth, self.table_name)
            activity_execution_list.append(activity_execution)
        scenario["activity_executions"] = activity_execution_list

        import experiment.experiment_service_relational
        experiment_service_relational = experiment.experiment_service_relational.ExperimentServiceRelational()
        experiment = experiment_service_relational.get_experiment(scenario["experiment_id"], depth, self.table_name)
        scenario["experiment"] = experiment
        return ScenarioOut(**scenario)

    def get_scenario_by_experiment(self, experiment_id: Union[int, str], depth: int = 0, source: str = ""):
        scenario_response = self.rdb_api_service.get_records_with_foreign_id(self.table_name, "experiment_id", experiment_id)
        if scenario_response["errors"] is not None:
            return NotFoundByIdModel(id=experiment_id, errors={"Scenario with such experiment id not found"})
        scenario = scenario_response["records"][0]
        import activity_execution.activity_execution_service_relational
        activity_execution_service_relational = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()

        activity_execution_list = []
        for activity_execution_id in scenario["activity_executions"]:
            activity_execution = activity_execution_service_relational.get_activity_execution(activity_execution_id, depth, self.table_name)
            activity_execution_list.append(activity_execution)
        scenario["activity_executions"] = activity_execution_list

        if source != Collections.EXPERIMENT:
            import experiment.experiment_service_relational
            experiment_service_relational = experiment.experiment_service_relational.ExperimentServiceRelational()
            experiment = experiment_service_relational.get_experiment(experiment_id, depth, self.table_name)
            scenario["experiment"] = experiment
        return ScenarioOut(**scenario)

    def change_order(self, order_change: OrderChangeIn):
        scenario = self.get_scenario_by_activity_execution_with_id_list(order_change.activity_execution_id)
        if type(scenario) is NotFoundByIdModel:
            return scenario
        if order_change.previous_id not in scenario["activity_executions"]:
            return NotFoundByIdModel(id=order_change.previous_id, errors={"Entity not found"})
        if order_change.activity_execution_id not in scenario["activity_executions"]:
            return NotFoundByIdModel(id=order_change.activity_execution_id, errors={"Entity not found"})
        scenario["activity_executions"].remove(order_change.activity_execution_id)
        index_of_previous_id = scenario["activity_executions"].index(order_change.previous_id)
        scenario["activity_executions"].insert(index_of_previous_id + 1, order_change.activity_execution_id)
        self.rdb_api_service.put(self.table_name, scenario["id"], scenario)
        return OrderChangeOut(**order_change.dict())

    def get_experiment_by_activity_execution(self, activity_execution_id: Union[int, str], depth: int = 0, source: str = ""):
        scenario = self.get_scenario_by_activity_execution_with_id_list(activity_execution_id)
        if type(scenario) is NotFoundByIdModel:
            return None
        import experiment.experiment_service_relational
        experiment_service_relational = experiment.experiment_service_relational.ExperimentServiceRelational()
        experiment = experiment_service_relational.get_experiment(scenario["experiment_id"], depth, self.table_name)
        return [experiment]

