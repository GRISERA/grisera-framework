from typing import Union
from measure.measure_model import MeasureIn, MeasureOut, MeasuresOut, MeasurePropertyIn, MeasureRelationIn
from measure.measure_service import MeasureService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections

class MeasureServiceRelational(MeasureService):
    
    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.MEASURE

    def save_measure(self, measure: MeasureIn):
        measure_data = {
            "measure_name_id": measure.measure_name_id,
            "datatype": measure.datatype,
            "range": measure.range,
            "unit": measure.unit
        }

        result = self.rdb_api_service.post(self.table_name, measure_data)
        if result["errors"] is not None:
            return MeasureOut(errors=result["errors"])
        return MeasureOut(**result["records"])
    
    def get_measures(self):
        results = self.rdb_api_service.get(self.table_name)
        return MeasuresOut(measures=results)
    
    def get_measure(self, measure_id: Union[int, str], depth: int = 0, source = ""):
        import measure_name.measure_name_service_relational
        measure_name_service = measure_name.measure_name_service_relational.MeasureNameServiceRelational()

        import time_series.time_series_service_relational
        time_series_service = time_series.time_series_service_relational.TimeSeriesServiceRelational()
        
        measure_dict = self.rdb_api_service.get_with_id(self.table_name, measure_id)
        if not measure_dict:
            return NotFoundByIdModel(id=measure_id, errors={"Entity not found."})
        
        if depth > 0:
            #if source != Collections.TIMESERIES:
                #TODO measure_dict["time_series"] = time_series_service.get_multiple_with_foreign_id(measure_id, depth - 1, self.table_name)
            if source != Collections.MEASURE_NAME:
                measure_dict["measure_name"] = measure_name_service.get_single_with_foreign_id(measure_dict["measure_name_id"], depth - 1, self.table_name)

        return MeasureOut(**measure_dict)
    
    def delete_measure(self, measure_id: Union[int, str]):
        get_response = self.get_measure(measure_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, measure_id)
        return get_response
    
    def update_measure(self, measure_id: Union[int, str], measure: MeasurePropertyIn):
        get_response = self.get_measure(measure_id)
        if type(get_response) != NotFoundByIdModel:
            put_result = self.rdb_api_service.put(self.table_name, measure_id,  measure.dict())
            if put_result["errors"] is not None:
                return MeasureOut(errors=put_result["errors"])
            return MeasureOut(**put_result["records"])
        return get_response

    def update_measure_relationships(self, measure_id: Union[int, str], measure: MeasureRelationIn):
        get_response = self.get_measure(measure_id)
        if type(get_response) != NotFoundByIdModel:
            put_result = self.rdb_api_service.put(self.table_name, measure_id, measure.dict())
            if put_result["errors"] is not None:
                return MeasureOut(errors=put_result["errors"])
            return MeasureOut(**put_result["records"])
        return get_response

    def get_multiple_with_foreign_id(self, id: Union[int, str], depth: int = 0, source = ""):
        import measure_name.measure_name_service_relational
        measure_name_service = measure_name.measure_name_service_relational.MeasureNameServiceRelational()
       
        import time_series.time_series_service_relational
        time_series_service = time_series.time_series_service_relational.TimeSeriesServiceRelational()

        measure_dict_list = self.rdb_api_service.get_records_with_foreign_id(self.table_name, source + "_id", id)
        if measure_dict_list["errors"] is not None:
            return []
        
        if depth <= 0:
            return measure_dict_list["records"]
        
        for measure_dict in measure_dict_list["records"]:
            #if source != Collections.TIMESERIES:
                #TODO measure_dict["time_series"] = time_series_service.get_multiple_with_foreign_id(measure_dict["id"], depth - 1, self.table_name)
            if source != Collections.MEASURE_NAME:
                measure_dict["measure_name"] = measure_name_service.get_single_with_foreign_id(measure_dict["measure_name_id"], depth - 1, self.table_name)
        
        return measure_dict_list["records"]

