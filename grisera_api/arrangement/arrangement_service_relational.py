from typing import Union
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, ArrangementsOut, BasicArrangementOut
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService


class ArrangementServiceRelational(ArrangementService):

    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = "Arrangement"

    def get_arrangements(self):
        results = self.rdb_api_service.get(self.table_name)
        arrangements = []
        for arrangement in results:
            arrangements.append(BasicArrangementOut(id=arrangement["id"], arrangement_type=arrangement["type"], arrangement_distance=arrangement["distance"]))
        return ArrangementsOut(arrangements=arrangements)

    def get_arrangement(self, arrangement_id: Union[int, str], depth: int = 0):
        arrangement = self.rdb_api_service.get_with_id(self.table_name, arrangement_id)
        if not arrangement:
            return NotFoundByIdModel(id=arrangement_id, errors="Entity not found")
        return ArrangementOut(id=arrangement["id"], arrangement_type=arrangement["type"], arrangement_distance=arrangement["distance"])
    