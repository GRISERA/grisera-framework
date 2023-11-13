import json

from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from time_series.time_series_model import TimeSeriesNodesOut, TimeSeriesOut, TimeSeriesIn, TimeSeriesPropertyIn, \
    TimeSeriesRelationIn, Type
from time_series.time_series_service import TimeSeriesService
from typing import Union, Optional, List
from starlette.datastructures import QueryParams
from time_series.transformation.multidimensional.TimeSeriesTransformationMultidimensional import \
    TimeSeriesTransformationMultidimensional


class TimeSeriesServiceRelational(TimeSeriesService):
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.TIMESERIES

    def get_time_series(self, time_series_id: Union[int, str], depth: int = 0,
                        signal_min_value: Optional[int] = None,
                        signal_max_value: Optional[int] = None, source: str = ""):
        print(signal_min_value)
        print("duuuupa")
        get_response = self.rdb_api_service.get_with_id(self.table_name, time_series_id)
        if get_response is None:
            return NotFoundByIdModel(id=time_series_id, errors={"Entity not found"})
        
        signal_table_name = Collections.SIGNAL_VALUES_EPOCH if get_response["type"] == Type.epoch else Collections.SIGNAL_VALUES_TIMESTAMP
        get_response["signal_values"] = self.rdb_api_service\
            .get_signal_values_in_range_with_foreign_id(signal_table_name, time_series_id, signal_max_value, signal_min_value)["records"]

        import observable_information.observable_information_service_relational
        import measure.measure_service_relational
        observable_information_service_relational = observable_information.observable_information_service_relational.ObservableInformationServiceRelational()
        measure_service_relational = measure.measure_service_relational.MeasureServiceRelational()

        get_response["observable_information_ids"] = observable_information_service_relational.get_ids_by_proxy_foreign_id(time_series_id, self.table_name)
        if depth > 0:
            if source != Collections.MEASURE:
                get_response["measure"] = measure_service_relational.get_measure(
                    get_response["measure_id"], depth - 1, self.table_name)
            if source != Collections.OBSERVABLE_INFORMATION:
                get_response["observable_informations"] = observable_information_service_relational.get_multiple_from_proxy_with_foreign_id(
                    time_series_id, depth - 1, self.table_name)
                
        return TimeSeriesOut(**get_response)

    def get_time_series_nodes(self, params: QueryParams = None):
        timeseries_nodes = self.rdb_api_service.get(self.table_name)
        return TimeSeriesNodesOut(time_series_nodes=timeseries_nodes)


    def save_time_series(self, time_series: TimeSeriesIn):
        if len(time_series.observable_information_ids) <= 0:
            return TimeSeriesOut(errors="Observable information ids must be provided", **time_series.dict())
        
        import observable_information.observable_information_service_relational
        observable_information_service_relational = observable_information.observable_information_service_relational.ObservableInformationServiceRelational()
        for observable_information_id in time_series.observable_information_ids:
            observable_information = observable_information_service_relational.get_observable_information(observable_information_id)
            if type(observable_information) is NotFoundByIdModel:
                return TimeSeriesOut(errors="Observable information with id " + str(observable_information_id) + " not found.", **time_series.dict())

        time_series_dict = time_series.dict()
        time_series_dict.pop("observable_information_ids")
        time_series_dict.pop("signal_values")
        if time_series.additional_properties is not None:
            time_series_dict["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in time_series.additional_properties
            ])

        saved_time_series_dict = self.rdb_api_service.post(self.table_name, time_series_dict)
        if saved_time_series_dict["errors"] is not None:
            return TimeSeriesOut(errors=saved_time_series_dict["errors"], **time_series.dict())

        signal_table_name = str()
        if time_series.type == Type.epoch:
            signal_table_name = Collections.SIGNAL_VALUES_EPOCH
        elif time_series.type == Type.timestamp:
            signal_table_name = Collections.SIGNAL_VALUES_TIMESTAMP
        else:
            return TimeSeriesOut(errors="Provided timeseries type is not allowed.", **time_series.dict())

        saved_time_series_dict["records"]["signal_values"] = list()
        for signal_value in time_series.signal_values:
            signal_value_dict = {
                "timeseries_id": saved_time_series_dict["records"]["id"],
                "value": signal_value.signal_value.value,
                "additional_properties": json.dumps([
                    {
                        "key": p.key,
                        "value": p.value
                    } for p in signal_value.signal_value.additional_properties if signal_value.signal_value.additional_properties is not None
                ])
            }
            if time_series.type == Type.epoch:
                signal_value_dict["start_timestamp"] = signal_value.start_timestamp
                signal_value_dict["end_timestamp"] = signal_value.end_timestamp
            elif time_series.type == Type.timestamp:
                signal_value_dict["timestamp"] = signal_value.timestamp

            saved_signal_dict = self.rdb_api_service.post(signal_table_name, signal_value_dict)
            if saved_signal_dict["errors"] is not None:
                self.delete_time_series(saved_time_series_dict["records"]["id"])
                return TimeSeriesOut(errors=saved_signal_dict["errors"], **time_series.dict())
            saved_time_series_dict["records"]["signal_values"].append(saved_signal_dict)

        for observable_information_id in time_series.observable_information_ids:
            observable_information_service_relational.add_proxy(observable_information_id, saved_time_series_dict["records"]["id"], self.table_name)

        saved_time_series_dict["records"]["observable_information_ids"] = time_series.observable_information_ids
        return TimeSeriesOut(**saved_time_series_dict["records"])

    def delete_time_series(self, time_series_id: Union[int, str]):
        result = self.get_time_series(time_series_id)
        if type(result) == NotFoundByIdModel:
            return result
        self.rdb_api_service.delete_with_id(self.table_name, time_series_id)
        return result

    def update_time_series(self, time_series_id: Union[int, str], time_series: TimeSeriesPropertyIn):
        if len(time_series.observable_information_ids) <= 0:
            return TimeSeriesOut(errors="Observable information ids must be provided", **time_series.dict())
        
        get_result = self.get_time_series(time_series_id)
        if type(get_result) == NotFoundByIdModel:
            return get_result
        time_series_dict = time_series.dict()
        if time_series.additional_properties is not None:
            time_series_dict["additional_properties"] = json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in time_series.additional_properties
            ])
        signal_values = []
        for signal_value in time_series.signal_values:
            signal_value_dict = signal_value.dict()
            signal_values.append(signal_value_dict)

        time_series_dict["signal_values"] = json.dumps(signal_values)
        result = self.rdb_api_service.put(self.table_name, time_series_id, time_series_dict)
        if result["errors"] is not None:
            return TimeSeriesOut(errors=result["errors"], **time_series.dict())
        result["records"]["observable_information_ids"] = get_result.observable_information_ids
        return TimeSeriesOut(**result["records"])

    def update_time_series_relationships(self, time_series_id: Union[int, str],
                                         time_series: TimeSeriesRelationIn):
        
        get_result = self.get_time_series(time_series_id)
        if type(get_result) == NotFoundByIdModel:
            return get_result
        get_result = get_result.dict()
        get_result.pop("errors")


        if time_series.observable_information_ids is not None:
            import observable_information.observable_information_service_relational
            observable_information_service_relational = observable_information.observable_information_service_relational.ObservableInformationServiceRelational()
            for observable_information_id in time_series.observable_information_ids:
                if type(observable_information_service_relational.get_observable_information(
                        observable_information_id)) is NotFoundByIdModel:
                    return TimeSeriesOut(errors="Observable information with id " + str(observable_information_id) + " not found", **get_result)
                
        if time_series.measure_id is not None:
            put_result = self.rdb_api_service.put(self.table_name, time_series_id, {"measure_id": time_series.measure_id})
            if put_result["errors"] is not None:
                print(put_result["errors"])
                return TimeSeriesOut(errors=put_result["errors"], **get_result)
        
        if time_series.observable_information_ids is not None:
            self.rdb_api_service.delete_by_column_value(Collections.OBSERVABLE_INFORMATION_TIMESERIES, self.table_name + "_id", time_series_id)
            for observable_information_id in time_series.observable_information_ids:
                observable_information_service_relational.add_proxy(observable_information_id, time_series_id, self.table_name)
        return self.get_time_series(time_series_id)
