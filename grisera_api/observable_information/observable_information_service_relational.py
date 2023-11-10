from typing import Union
from models.not_found_model import NotFoundByIdModel
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut, ObservableInformationsOut
from observable_information.observable_information_service import ObservableInformationService
from rdb_api_service import RdbApiService, Collections


class ObservableInformationServiceRelational(ObservableInformationService):
    
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.OBSERVABLE_INFORMATION

    def save_observable_information(self, observable_information: ObservableInformationIn):
        saved_observable_information_dict = self.rdb_api_service.post(self.table_name, observable_information.dict())["records"]
        return ObservableInformationOut(** saved_observable_information_dict)
    
    def get_observable_informations(self):
        results = self.rdb_api_service.get(self.table_name)
        return ObservableInformationsOut(observable_informations=results)
    
    def get_observable_information(self, observable_information_id: Union[int, str], depth: int = 0, source: str = ""):
        observable_information_dict = self.rdb_api_service.get_with_id(self.table_name, observable_information_id)
        if not observable_information_dict:
            return NotFoundByIdModel(id=observable_information_id, errors={"Entity not found"})
        
        # import life_activity.life_activity_service_relational
        import modality.modality_service_relational
        import recording.recording_service_relational
        # import time_series.time_series_service_relational
        # life_activity_service = life_activity.life_activity_service_relational.LifeActivityServiceRelational()
        modality_service = modality.modality_service_relational.ModalityServiceRelational()
        recording_service = recording.recording_service_relational.RecordingServiceRelational()
        # time_series_service = time_series.time_series_service_relational.TimeSeriesServiceRelational()

        if depth > 0:
        #     if source != Collections.LIFE_ACTIVITY:
        #         observable_information_dict["life_activity"] = life_activity_service.get_life_activity(observable_information_dict["life_activity_id"], depth - 1, self.table_name)
            if source != Collections.MODALITY:
                observable_information_dict["modality"] = modality_service.get_modality(observable_information_dict["modality_id"], depth - 1, self.table_name)
            if source != Collections.RECORDING:
                observable_information_dict["recording"] = recording_service.get_recording(observable_information_dict["recording_id"], depth - 1, self.table_name)
        #     if source != Collections.TIMESERIES:
        #         observable_information_dict["timeSeries"] = time_series_service.get_multiple_with_foreign_id(id, depth - 1, self.table_name)
            
        return ObservableInformationOut(**observable_information_dict)
    
    def delete_observable_information(self, observable_information_id: Union[int, str]):
        result = self.get_observable_information(observable_information_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, observable_information_id)
        return result
    
    def update_observable_information_relationships(self, observable_information_id: Union[int, str],
                                                    observable_information: ObservableInformationIn):
        result = self.get_observable_information(observable_information_id)
        if type(result) == NotFoundByIdModel:
            return result
        
        put_result = self.rdb_api_service.put(self.table_name, observable_information_id, observable_information.dict())
        if put_result["errors"] is not None:
            return ObservableInformationOut(errors = put_result["errors"])
        return ObservableInformationOut(**put_result["records"])
    
    def get_multiple_with_foreign_id(self, id: Union[int, str], depth: int = 0, source = ""):
        #import life_activity.life_activity_service_relational
        import modality.modality_service_relational
        import recording.recording_service_relational
        #import time_series.time_series_service_relational
        #life_activity_service = life_activity.life_activity_service_relational.LifeActivityServiceRelational()
        modality_service = modality.modality_service_relational.ModalityServiceRelational()
        recording_service = recording.recording_service_relational.RecordingServiceRelational()
        #time_series_service = time_series.time_series_service_relational.TimeSeriesServiceRelational()

        observable_information_dict_list = self.rdb_api_service.get_records_with_foreign_id(self.table_name, source + "_id", id)
        if observable_information_dict_list["errors"] is not None:
            return []
        
        if depth <= 0:
            return observable_information_dict_list["records"]
        
        for observable_information_dict in observable_information_dict_list["records"]:
            #if source != Collections.LIFE_ACTIVITY:
                #observable_information_dict["life_activity"] = life_activity_service.get_life_activity(observable_information_dict["life_activity_id"], depth - 1, self.table_name)
            if source != Collections.MODALITY:
                observable_information_dict["modality"] = modality_service.get_modality(observable_information_dict["modality_id"], depth - 1, self.table_name)
            if source != Collections.RECORDING:
                observable_information_dict["recording"] = recording_service.get_recording(observable_information_dict["recording_id"], depth - 1, self.table_name)
            #if source != Collections.TIMESERIES:
                #observable_information_dict["timeSeries"] = time_series_service.get_multiple_with_foreign_id(id, depth - 1, self.table_name)
        
        return observable_information_dict_list["records"]
    