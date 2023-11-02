from typing import Union
from measure.measure_model import MeasureIn, MeasureOut, MeasuresOut, MeasurePropertyIn, MeasureRelationIn
from measure.measure_service import MeasureService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService
from time_series.time_series_service_relational import TimeSeriesService
from measure_name.measure_name_service_relational import MeasureNameService

class MeasureServiceRelational(MeasureService):
    rdb_api_service = RdbApiService()
    table_name = "measure"

    def __init__(self):
        self.time_series_service = TimeSeriesService()
        self.measure_name_service = MeasureNameService()

    def save_measure(self, measure: MeasureIn):
        measure_data = {
            "measure_name_id": measure.measure_name_id,
            "datatype": measure.datatype,
            "range": measure.range,
            "unit": measure.unit
        }

        saved_measure_dict = self.rdb_api_service.post(self.table_name, measure_data)

        return MeasureOut(**saved_measure_dict)
    
    def get_measures(self):
        results = self.rdb_api_service.get(self.table_name)
        return MeasuresOut(measures=results)
    
    def get_measure(self, measure_id: Union[int, str], depth: int = 0, source = ""):
        measure_dict = self.rdb_api_service.get_with_id(self.table_name, measure_id)
        if not measure_dict:
            return NotFoundByIdModel(id=measure_id, errors={"Entity not found."})
        
        if depth > 0:
            # not implemented yet
            if source != "time_series":
                measure_dict["time_series"] = self.time_series_service.get_multiple_with_foreign_id(measure_id, depth - 1, self.table_name)
            if source != "measure_name":
                measure_dict["measure_name"] = self.measure_name_service.get_single(measure_dict["measure_name_id"], depth - 1, self.table_name)

        return MeasureOut(**measure_dict)
    
    def delete_measure(self, measure_id: Union[int, str]):
        get_response = self.get_measure(measure_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, measure_id)
        return get_response
    
    def update_measure(self, measure_id: Union[int, str], measure: MeasurePropertyIn):
        get_response = self.get_measure(measure_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.put(self.table_name, measure_id, measure.dict())
        return self.get_measure(measure_id)

    def update_measure_relationships(self, measure_id: Union[int, str], measure: MeasureRelationIn):
        get_response = self.get_measure(measure_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.put(self.table_name, measure_id, measure.dict())
        return self.get_measure(measure_id)