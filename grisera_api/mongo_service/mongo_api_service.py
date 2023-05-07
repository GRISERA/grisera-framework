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
        Create new document
        """
        collection_name = get_collection_name(type(data_in))
        data_as_dict = data_in.dict()
        self._fix_query_ids(data_as_dict)
        created_id = self.db[collection_name].insert_one(data_as_dict).inserted_id
        return str(created_id)

    def get_document(self, id: Union[str, int], model_class, *args, **kwargs):
        """
        Load single document
        """
        collection_name = get_collection_name(model_class)
        result_dict = self.db[collection_name].find_one(
            {self.MONGO_ID_FIELD: ObjectId(id)}, *args, **kwargs
        )

        if result_dict is None:
            return NotFoundByIdModel(
                id=id,
                errors={"errors": "document not found"},
            )

        self._update_mongo_output_id(result_dict)
        return result_dict

    def get_documents(self, model_class, query: dict = {}, *args, **kwargs):
        """
        Load many documents
        """
        collection_name = get_collection_name(model_class)
        self._fix_query_ids(query)
        results = list(self.db[collection_name].find(query, *args, **kwargs))

        [self._update_mongo_output_id(result) for result in results]

        return results

    def update_document(self, id: Union[str, int], data_to_update: BaseModel):
        """
        Update document
        """
        collection_name = get_collection_name(type(data_to_update))
        data_as_dict = data_to_update.dict()
        self._update_document_with_dict(collection_name, id, data_as_dict)

    def _update_document_with_dict(
        self, collection_name: str, id: Union[str, int], new_document: dict
    ):
        """
        Update document with new document as dict
        """
        self._update_mongo_input_id(new_document)
        id = ObjectId(id)
        self.db[collection_name].replace_one(
            {self.MONGO_ID_FIELD: id},
            new_document,
        )

    def delete_document(self, object_to_delete: BaseModel):
        """
        Delete document in collection
        """
        id = ObjectId(object_to_delete.id)
        collection_name = get_collection_name(type(object_to_delete))
        self.db[collection_name].delete_one({self.MONGO_ID_FIELD: id})
        return id

    @staticmethod
    def _add_additional_properties_to_dict(data_dict: dict):
        if data_dict["additional_properties"] is None:
            return
        for additional_property in data_dict["additional_properties"]:
            data_dict[additional_property["key"]] = data_dict[
                additional_property["value"]
            ]
        del data_dict["additional_properties"]

    def _update_mongo_input_id(self, mongo_input: dict):
        if self.MODEL_ID_FIELD in mongo_input:
            mongo_input[self.MONGO_ID_FIELD] = ObjectId(
                mongo_input[self.MODEL_ID_FIELD]
            )
        del mongo_input[self.MODEL_ID_FIELD]
        self._fix_query_ids(mongo_input)

    def _update_mongo_output_id(self, mongo_output: dict):
        if self.MONGO_ID_FIELD in mongo_output:
            mongo_output[self.MODEL_ID_FIELD] = str(mongo_output[self.MONGO_ID_FIELD])
        del mongo_output[self.MONGO_ID_FIELD]
        self._fix_output_ids(mongo_output)

    def _fix_query_ids(self, query):
        for field, value in query.items():
            if type(value) is dict:
                self._fix_query_ids(value)
            elif self._field_is_id(field):
                query[field] = ObjectId(query[field])

    def _fix_output_ids(self, result):
        """
        Perform deep iteration over query result and parser all ObjectId's fields to str
        """
        if type(result) is not dict:
            return
        for field, value in result.items():
            if type(value) is dict:
                self._fix_output_ids(value)
            elif type(value) is list:
                for list_elem in value:
                    self._fix_output_ids(list_elem)
            elif self._field_is_id(field):
                result[field] = str(result[field])

    @staticmethod
    def _field_is_id(field):
        if type(field) is not str:
            return False
        return field == "id" or (len(field) >= 3 and field[-3:] in ("_id", ".id"))


mongo_api_service = MongoApiService()
