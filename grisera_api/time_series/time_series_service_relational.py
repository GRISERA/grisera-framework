import json
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from time_series.time_series_model import TimeSeriesIn, TimeSeriesOut
from time_series.time_series_service import TimeSeriesService


class TimeSeriesServiceRelational(TimeSeriesService):
    
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.TIMESERIES

    def save_time_series(self, time_series: TimeSeriesIn):
        time_series_dict = time_series.dict()
        if time_series.additional_properties is not None:
            time_series_dict["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in time_series.additional_properties
            ])
        print(time_series_dict)
        saved_time_series_dict = self.rdb_api_service.post(self.table_name, time_series_dict)
        print(saved_time_series_dict)
        if saved_time_series_dict["errors"] is not None:
            return TimeSeriesOut(errors=saved_time_series_dict["errors"])
        return TimeSeriesOut(**saved_time_series_dict["records"])