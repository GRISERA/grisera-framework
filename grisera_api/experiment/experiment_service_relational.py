import json
from typing import Union
from experiment.experiment_model import ExperimentIn, ExperimentOut, ExperimentsOut
from experiment.experiment_service import ExperimentService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from activity_execution.activity_execution_service import ActivityExecutionService

class ExperimentServiceRelational(ExperimentService):
    

    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.EXPERIMENT


    def save_experiment(self, experiment: ExperimentIn):
        experiment_data = experiment.dict()
        if experiment.additional_properties is not None:
            experiment_data["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in experiment.additional_properties
            ])

        saved_experiment_dict = self.rdb_api_service.post(self.table_name, experiment_data)["records"]

        return ExperimentOut(**saved_experiment_dict)
    

    def get_experiments(self):
        results = self.rdb_api_service.get(self.table_name)
        return ExperimentsOut(experiments=results)
    

    def get_experiment(self, experiment_id: Union[int, str], depth: int = 0, source = ""):
        experiment_dict = self.rdb_api_service.get_with_id(self.table_name, experiment_id)
        if not experiment_dict:
            return NotFoundByIdModel(id=experiment_id, errors={"Entity not found."})
        
        import activity_execution.activity_execution_service_relational
        activity_executions_service = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()
        
        if depth > 0 and source != Collections.ACTIVITY_EXECUTION:
                experiment_dict["activity_executions"] == activity_executions_service.get_multiple_with_foreign_id(experiment_id, depth - 1, self.table_name)

        return ExperimentOut(**experiment_dict)
        

    def delete_experiment(self, experiment_id: Union[int, str]):
        get_response = self.get_experiment(experiment_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, experiment_id)
        return get_response
    
    
    def update_experiment(self, experiment_id: Union[int, str], experiment: ExperimentIn):
        experiment_data = experiment.dict()
        if experiment.additional_properties is not None:
            experiment_data["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in experiment.additional_properties
            ])

        get_response = self.get_experiment(experiment_id)
        if type(get_response) == NotFoundByIdModel:
            return get_response
        
        put_result = self.rdb_api_service.put(self.table_name, experiment_id, experiment_data)
        if put_result["errors"] is not None:
            return ExperimentOut(errors=put_result["errors"])
        return ExperimentOut(**put_result["records"])
