from typing import Union
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_model import ArrangementOut, ArrangementIn, ArrangementsOut
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from activity_execution.activity_execution_service_relational import ActivityExecutionServiceRelational

class ArrangementServiceRelational(ArrangementService):

    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.ARRANGEMENT
        self.activity_execution_service = ActivityExecutionServiceRelational()


    def get_arrangements(self):
        results = self.rdb_api_service.get(self.table_name)
        return  ArrangementsOut(arrangements=results)
    

    def get_arrangement(self, arrangement_id: Union[int, str], depth: int = 0, source: str = ""):
        arrangement_dict = self.rdb_api_service.get_with_id(self.table_name, arrangement_id)
        if not arrangement_dict:
            return NotFoundByIdModel(id=arrangement_id, errors={"Entity not found."})
        
        # import activity_execution.activity_execution_service_relational
        # activity_execution_service = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()

        # if depth > 0 and source != Collections.ACTIVITY_EXECUTION:
        #         arrangement_dict["activity_executions"] = activity_execution_service.get_multiple_with_foreign_id(arrangement_id, depth - 1, self.table_name)

        return ArrangementOut(**arrangement_dict)
    

    def get_multiple_with_foreign_id(self, id: Union[int, str], depth: int = 0, source: str = ""):
        arrangement_dict_list = self.rdb_api_service.get_records_with_foreign_id(self.table_name, "{}_id".format(source), id)
        if arrangement_dict_list["errors"] is not None:
            return []
        
        if depth <= 0:
            return arrangement_dict_list["records"]
        
        # import activity_execution.activity_execution_service_relational
        # activity_execution_service = activity_execution.activity_execution_service_relational.ActivityExecutionServiceRelational()

        # for arrangement_dict in arrangement_dict_list["records"]:
            # if source != Collections.ACTIVITY_EXECUTION:
            #     arrangement_dict["activity_executions"] = activity_execution_service.get_multiple_with_foreign_id(arrangement_dict["id"], depth - 1, self.table_name)
        
        return arrangement_dict_list["records"]