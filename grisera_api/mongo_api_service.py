from typing import Union
from pydantic import BaseModel
from pymongo import MongoClient
from grisera_api.models.not_found_model import NotFoundByIdModel

from mongodb_api_config import mongo_api_address, mongo_database_name


class MongoApiService:
    """
    Object that handles communication with mongodb
    """

    def __init__(self):
        """
        Connect to MongoDB database
        """
        self.client = MongoClient(mongo_api_address)
        self.db = self.client[mongo_database_name]

    def create_document(self, collection_name: str, data_in: BaseModel):
        """
        Create new document, with "additional properties" field handling
        """
        data_as_dict = data_in.dict()
        if "additional_properties" in data_as_dict:
            self._add_additional_properties_to_dict(data_as_dict)
        return self.db[collection_name].insert_one(data_as_dict)

    def load_document(
        self, id: Union[str, int], collection_name: str, model_class: BaseModel
    ):
        """
        Load single document, with "additional properties" field handling
        """
        result_dict = self.db[collection_name].find_one({"id": id})
        if result_dict is None:
            return NotFoundByIdModel(
                id=id,
                errors={"errors": "document not found"},
            )

        expected_fields = model_class.__fields__.keys()
        if "additional_properties" in expected_fields:
            self._move_additional_properties_to_array(result_dict, expected_fields)
        return result_dict

    def load_documents(self, query: dict, collection_name: str, model_class: BaseModel):
        """
        Load many documents, with "additional properties" field handling
        """
        results = self.db[collection_name].find(query)

        expected_fields = model_class.__fields__.keys()
        if "additional_properties" in expected_fields:
            for result in results:
                self._move_additional_properties_to_array(result, expected_fields)

        return results

    def update_document(
        self, collection_name: str, id: Union[str, int], data_to_update: BaseModel
    ):
        """
        Update document, with "additional properties" field handling
        """
        data_as_dict = data_to_update.dict()
        if "additional_properties" in data_to_update:
            self._add_additional_properties_to_dict(data_as_dict)
        self.update_document_with_dict(collection_name, id, data_as_dict)

    def update_document_with_dict(
        self, collection_name: str, id: Union[str, int], data_to_update: dict
    ):
        """
        Update document with data as dict
        """
        self.db[collection_name].update_one(
            {"id": id},
            data_to_update,
        )

    def delete_document(self, id: Union[str, int], collection_name: str):
        """
        Delete document in collection
        """
        self.db[collection_name].delete_one({"id": id})
        return id

    @staticmethod
    def _add_additional_properties_to_dict(data_dict: dict):
        for additional_property in data_dict["additional_properties"]:
            data_dict[additional_property["key"]] = data_dict[
                additional_property["value"]
            ]
        del data_dict["additional_properties"]

    @staticmethod
    def _move_additional_properties_to_array(result_dict: dict, expected_fields):
        additional_properties = []
        for key, value in {**result_dict}.items():
            if key in expected_fields:
                continue
            additional_properties.append({"key": key, "value": value})
            del result_dict[key]
        result_dict["additional_properties"] = additional_properties


mongo_api_service = MongoApiService()
