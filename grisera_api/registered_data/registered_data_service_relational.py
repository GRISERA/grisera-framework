from typing import Union
from registered_channel.registered_channel_service import RegisteredChannelService
from models.not_found_model import NotFoundByIdModel
from rdb_api_service import RdbApiService, Collections
from registered_data.registered_data_model import RegisteredDataIn, RegisteredDataNodesOut, RegisteredDataOut
from registered_data.registered_data_service import RegisteredDataService


class RegisteredDataServiceRelational(RegisteredDataService):
    
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.registered_channel_service = RegisteredChannelService()
        self.table_name = Collections.REGISTERED_DATA
    

    def save_registered_data(self, registered_data: RegisteredDataIn):
        registered_data_dict = {
            "source": registered_data.source,
            "additional_properties": registered_data.additional_properties
        }
        saved_registered_data_dict = self.rdb_api_service.post(self.table_name, registered_data_dict)
        return RegisteredDataOut(**saved_registered_data_dict)


    def get_registered_data_nodes(self):
        results = self.rdb_api_service.get(self.table_name)
        return RegisteredDataNodesOut(registered_data_nodes=results)


    def get_registered_data(self, registered_data_id: Union[int, str], depth: int = 0, source: str = ""):
        registered_data_dict = self.rdb_api_service.get_with_id(self.table_name, registered_data_id)
        if not registered_data_dict:
            return NotFoundByIdModel(id=registered_data_id, errors={"Entity not found"})
        if depth > 0 and source != Collections.REGISTERED_CHANNEL:
            registered_data_dict["registered_channels"] = self.registered_channel_service.get_multiple_with_foreign_id(registered_data_id, depth - 1, self.table_name)
        return RegisteredDataOut(**registered_data_dict)


    def delete_registered_data(self, registered_data_id: Union[int, str]):
        result = self.get_registered_data(registered_data_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, registered_data_id)
        return result


    def update_registered_data(self, registered_data_id: Union[int, str], registered_data: RegisteredDataIn):
        result = self.get_registered_data(registered_data_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.put(self.table_name, registered_data_id, registered_data.dict())
        return self.get_registered_data(registered_data_id)
    

    def get_single_with_foreign_id(self, registered_data_id, depth: int = 0, source: str = ""):
        if depth > 0 and source != Collections.REGISTERED_CHANNEL:
            result = self.rdb_api_service.get_with_id(self.table_name, registered_data_id)
            return result
        return None
    