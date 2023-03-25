from typing import Union
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

from models.not_found_model import NotFoundByIdModel
from mongo_service.collection_mapping import get_collection_name
from mongo_service.mongodb_api_config import mongo_api_address, mongo_database_name


class MongoApiService:
    """
    Object that handles communication with mongodb
    """

    MONGO_ID_FIELD = "_id"
    MODEL_ID_FIELD = "id"

    def __init__(self):
        """
        Connect to MongoDB database
        """
        self.client = MongoClient(mongo_api_address)
        self.db = self.client[mongo_database_name]

    def create_document(self, data_in: BaseModel):
        """
        Create new document, with "additional properties" field handling
        """
        collection_name = get_collection_name(type(data_in))
        data_as_dict = data_in.dict()
        if "additional_properties" in data_as_dict:
            self._add_additional_properties_to_dict(data_as_dict)
        return self.db[collection_name].insert_one(data_as_dict).inserted_id

    def get_document(self, id: Union[str, int], model_class, fiedls_to_exclude=[]):
        """
        Load single document, with "additional properties" field handling
        """
        collection_name = get_collection_name(model_class)
        field_projection = self._get_field_projection(fiedls_to_exclude)
        result_dict = self.db[collection_name].find_one(
            {self.MONGO_ID_FIELD: id}, field_projection
        )
        if result_dict is None:
            return NotFoundByIdModel(
                id=id,
                errors={"errors": "document not found"},
            )

        self._update_mongo_output_id(result_dict)
        expected_fields = model_class.__fields__.keys()
        if "additional_properties" in expected_fields:
            self._move_additional_properties_to_array(result_dict, expected_fields)
        return result_dict

    def get_documents(self, model_class, query: dict = {}, fiedls_to_exclude=[]):
        """
        Load many documents, with "additional properties" field handling
        """
        collection_name = get_collection_name(model_class)
        field_projection = self._get_field_projection(fiedls_to_exclude)
        results = self.db[collection_name].find(query, field_projection)

        [self._update_mongo_output_id(result) for result in result]
        expected_fields = model_class.__fields__.keys()
        if "additional_properties" in expected_fields:
            for result in results:
                self._move_additional_properties_to_array(result, expected_fields)

        return results

    def update_document(self, id: Union[str, int], data_to_update: BaseModel):
        """
        Update document, with "additional properties" field handling
        """
        collection_name = get_collection_name(type(data_to_update))
        data_as_dict = data_to_update.dict()
        if "additional_properties" in data_to_update:
            self._add_additional_properties_to_dict(data_as_dict)
        self._update_document_with_dict(collection_name, id, data_as_dict)

    def _update_document_with_dict(
        self, collection_name: str, id: Union[str, int], data_to_update: dict
    ):
        """
        Update document with data as dict
        """
        self._update_mongo_input_id(data_to_update)
        self.db[collection_name].update_one(
            {self.MONGO_ID_FIELD: id},
            data_to_update,
        )

    def delete_document(self, object_to_delete: BaseModel):
        """
        Delete document in collection
        """
        id = object_to_delete.id
        collection_name = get_collection_name(type(object_to_delete))
        self.db[collection_name].delete_one({self.MONGO_ID_FIELD: id})
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

    def _update_mongo_input_id(self, mongo_input: dict):
        if self.MODEL_ID_FIELD in mongo_input:
            mongo_input[self.MONGO_ID_FIELD] = mongo_input[self.MODEL_ID_FIELD]
        del mongo_input[self.MODEL_ID_FIELD]

    def _update_mongo_output_id(self, mongo_output: dict):
        output_id = mongo_output[self.MONGO_ID_FIELD]
        if self.MONGO_ID_FIELD in mongo_output:
            mongo_output[self.MODEL_ID_FIELD] = str(mongo_output[self.MONGO_ID_FIELD])
        del mongo_output[self.MONGO_ID_FIELD]

    def _get_field_projection(self, fields_to_exclude):
        return {field: 0 for field in fields_to_exclude}


mongo_api_service = MongoApiService()
