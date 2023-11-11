import json
from typing import Union

from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionRelationIn, \
    ActivityExecutionsOut, ActivityExecutionOut
from activity_execution.activity_execution_service import ActivityExecutionService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections


class ActivityExecutionServiceRelational(ActivityExecutionService):
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.ACTIVITY_EXECUTION

    def save_activity_execution(self, activity_execution: ActivityExecutionIn):
        activity_execution_dict = activity_execution.dict()
        if activity_execution.additional_properties is not None:
            activity_execution_dict["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in activity_execution.additional_properties
            ])
        result =  self.rdb_api_service.post(self.table_name, activity_execution_dict)
        if result["errors"] is not None:
            return ActivityExecutionOut(errors=result["errors"])
        return ActivityExecutionOut(**result["records"])

    def get_activity_executions(self):
        results = self.rdb_api_service.get(self.table_name)
        return ActivityExecutionsOut(activity_executions=results)

    def get_activity_execution(self, activity_execution_id: Union[int, str], depth: int = 0, source: str = ""):
        activity_execution = self.rdb_api_service.get_with_id(self.table_name, activity_execution_id)
        if not activity_execution:
            return NotFoundByIdModel(id=activity_execution_id, errors={"Entity not found"})
        if depth > 0:
            import activity.activity_service_relational
            import participation.participation_service_relational
            import experiment.experiment_service_relational
            import arrangement.arrangement_service_relational
            activity_service_relational = activity.activity_service_relational.ActivityServiceRelational()
            participation_service_relational = participation.participation_service_relational.ParticipationServiceRelational()
            experiment_service_relational = experiment.experiment_service_relational.ExperimentServiceRelational()
            arrangement_service_relational = arrangement.arrangement_service_relational.ArrangementServiceRelational()

            #TODO if source != Collections.ACTIVITY:
            #     activity_execution["activity"] = activity_service_relational.get_activity(
            #         activity_execution["activity_id"], depth - 1, self.table_name)
            # if source != Collections.PARTICIPATION:
            #     activity_execution["participations"] = participation_service_relational.get_multiple_with_foregn_id(
            #         activity_execution["participation_id"], depth - 1, self.table_name)
            # if source != Collections.EXPERIMENT:
            #     activity_execution["experiments"] = experiment_service_relational.get_multiple_with_foregn_id(
            #         activity_execution["experiment_id"], depth - 1, self.table_name)
            # if source != Collections.ARRANGEMENT:
            #     activity_execution["arrangements"] = arrangement_service_relational.get_arrangement(
            #         activity_execution["arrangement_id"], depth - 1, self.table_name)
        return ActivityExecutionOut(**activity_execution)

    def delete_activity_execution(self, activity_execution_id: Union[int, str]):
        result = self.get_activity_execution(activity_execution_id)
        if type(result) == NotFoundByIdModel:
            return result

        import scenario.scenario_service_relational
        scenario_service_relational = scenario.scenario_service_relational.ScenarioServiceRelational()

        scenario_service_relational.delete_activity_execution(activity_execution_id)
        self.rdb_api_service.delete_with_id(self.table_name, activity_execution_id)
        return result

    def update_activity_execution(self, activity_execution_id: Union[int, str], activity_execution: ActivityExecutionIn):
        activity_execution_dict = activity_execution.dict()
        if activity_execution.additional_properties is not None:
            activity_execution_dict["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in activity_execution.additional_properties
            ])
        result = self.get_activity_execution(activity_execution_id)
        if type(result) is NotFoundByIdModel:
            return result
        put_result = self.rdb_api_service.put(self.table_name, activity_execution_id, activity_execution_dict)
        if put_result["errors"] is not None:
            return ActivityExecutionOut(errors=put_result["errors"])
        return ActivityExecutionOut(**put_result["records"])

    def update_activity_execution_relationships(self, activity_execution_id: Union[int, str],
                                                activity_execution: ActivityExecutionRelationIn):
        activity_execution_dict = activity_execution.dict()
        result = self.get_activity_execution(activity_execution_id)
        if type(result) is NotFoundByIdModel:
            return result
        put_result = self.rdb_api_service.put(self.table_name, activity_execution_id, activity_execution_dict)
        if put_result["errors"] is not None:
            return ActivityExecutionOut(errors=put_result["errors"])
        return ActivityExecutionOut(**put_result["records"])