from typing import Union
from experiment.experiment_model import ExperimentIn, ExperimentOut, ExperimentsOut
from experiment.experiment_service import ExperimentService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService
from activity_execution.activity_execution_service import ActivityExecutionService

class ExperimentServiceRelational(ExperimentService):
    rdb_api_service = RdbApiService()
    table_name = "experiment"

    def __init__(self):
        self.activity_executions_service = ActivityExecutionService()

    def save_experiment(self, experiment: ExperimentIn):
        experiment_data = {
            "experiment_name": experiment.experiment_name,
            "additional_properties": {[
                {
                    "key": p.key,
                    "value": p.value
                } for p in experiment.additional_properties
            ]}
        }

        print(experiment_data)

        saved_experiment_dict = self.rdb_api_service.post(self.table_name, experiment_data)

        return ExperimentOut(**saved_experiment_dict)
    
    def get_experiments(self):
        results = self.rdb_api_service.get(self.table_name)
        return ExperimentsOut(experiments=results)
    
    def get_experiment(self, experiment_id: Union[int, str], depth: int = 0, source = ""):
        experiment_dict = self.rdb_api_service.get_with_id(self.table_name, experiment_id)
        if not experiment_dict:
            return NotFoundByIdModel(id=experiment_id, errors={"Entity not found."})
        
        if depth > 0:
            if source != "activity_execution":
                experiment_dict["activity_executions"] == self.activity_executions_service.get_multiple_with_foreign_id(experiment_id, depth - 1, self.table_name)

        return ExperimentOut(**experiment_dict)
        
    def delete_experiment(self, experiment_id: Union[int, str]):
        get_response = self.get_appearance(experiment_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, experiment_id)
        return get_response