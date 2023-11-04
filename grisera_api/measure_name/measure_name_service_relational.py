from typing import Union
from measure.measure_service import MeasureService
from models.not_found_model import NotFoundByIdModel
from measure_name.measure_name_model import MeasureNameIn, MeasureNameOut, MeasureNamesOut
from rdb_api_service import RdbApiService, Collections
from measure_name.measure_name_service import MeasureNameService


class MeasureNameServiceRelational(MeasureNameService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.measure_service = MeasureService()
        self.table_name = Collections.MEASURE_NAME

    def save_measure_name(self, measure_name: MeasureNameIn):
        measure_name_dict = {
            "name": measure_name.name,
            "type": measure_name.type
        }
        saved_measure_name_dict = self.rdb_api_service.post(self.table_name, measure_name_dict)
        return MeasureNameOut(**saved_measure_name_dict)

    def get_measure_names(self):
        results = self.rdb_api_service.get(self.table_name)
        return MeasureNamesOut(measure_names=results)

    def get_measure_name(self, measure_name_id: Union[int, str], depth: int = 0, source: str = ""):
        measure_name_dict = self.rdb_api_service.get_with_id(self.table_name, measure_name_id)
        if not measure_name_dict:
            return NotFoundByIdModel(id=measure_name_id, errors={"Entity not found"})
        if depth > 0 and source != Collections.MEASURE:
            measure_name_dict["measures"] = self.measure_service.get_multiple_with_foreign_id(measure_name_id, depth - 1, self.table_name)
        return MeasureNameOut(**measure_name_dict)

    def get_single_with_foreign_id(self, measure_name_id: Union[int, str], depth: int = 0, source: str = ""):
        if depth > 0 and source != Collections.MEASURE:
            result = self.rdb_api_service.get_with_id(self.table_name, measure_name_id)
            return result
        return None
    