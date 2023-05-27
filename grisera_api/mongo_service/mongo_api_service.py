from typing import Union
from pydantic import BaseModel
import pymongo
from bson import ObjectId
from datetime import datetime

from time_series.time_series_model import TimeSeriesIn
from models.not_found_model import NotFoundByIdModel
from mongo_service.collection_mapping import get_collection_name
from mongo_service.mongodb_api_config import mongo_api_address, mongo_database_name


class MongoApiService:
    """
    Object that handles direct communication with mongodb
    """

    MONGO_ID_FIELD = "_id"
    MODEL_ID_FIELD = "id"
    TIMESTAMP_FIELD = "timestamp"
    METADATA_FIELD = "metadata"

    def __init__(self):
        """
        Connect to MongoDB database
        """
        self.client = pymongo.MongoClient(mongo_api_address)
        self.db = self.client[mongo_database_name]

    def create_document(self, data_in: BaseModel):
        """
        Create new document. Id fields are converted to ObjectId type.
        """
        collection_name = get_collection_name(type(data_in))
        data_as_dict = data_in.dict()
        self._fix_input_ids(data_as_dict)
        created_id = self.db[collection_name].insert_one(data_as_dict).inserted_id
        return str(created_id)

    def get_document(self, id: Union[str, int], collection_name: str, *args, **kwargs):
        """
        Load single document. Output id fields are converted from ObjectId type to str.
        """
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

    def get_documents(self, collection_name: str, query: dict = {}, *args, **kwargs):
        """
        Load many documents. Output id fields are converted from ObjectId type to str.
        """
        self._fix_input_ids(query)
        results = list(self.db[collection_name].find(query, *args, **kwargs))

        [self._update_mongo_output_id(result) for result in results]

        return results

    def update_document(self, id: Union[str, int], data_to_update: BaseModel):
        """
        Update document.
        """
        collection_name = get_collection_name(type(data_to_update))
        data_as_dict = data_to_update.dict()
        self._update_document_with_dict(collection_name, id, data_as_dict)

    def _update_document_with_dict(
        self, collection_name: str, id: Union[str, int], new_document: dict
    ):
        """
        Update document with new document as dict. Id fields are converted to ObjectId type.
        """
        self._update_mongo_input_id(new_document)
        id = ObjectId(id)
        self.db[collection_name].replace_one(
            {self.MONGO_ID_FIELD: id},
            new_document,
        )

    def delete_document(self, object_to_delete: BaseModel):
        """
        Delete document in collection. Given model must have id field.
        """
        id_str = getattr(object_to_delete, self.MODEL_ID_FIELD, None)
        if id_str is None:
            raise TypeError(
                f"Given model object does not have '{self.MODEL_ID_FIELD}' field"
            )
        id = ObjectId(id_str)
        collection_name = get_collection_name(type(object_to_delete))
        self.db[collection_name].delete_one({self.MONGO_ID_FIELD: id})
        return id

    def create_time_series(self, time_series_in: TimeSeriesIn):
        collection_name = get_collection_name(type(time_series_in))
        signal_values = time_series_in.signal_values
        time_series_in.signal_values = (
            []
        )  # avoid necessary parsing of signal values to dict
        time_series_dict = time_series_in.dict()
        time_series_dict.pop("signal_values")
        metadata = time_series_dict
        self._fix_input_ids(metadata)
        inserted_documents = [
            {
                self.TIMESTAMP_FIELD: datetime.utcfromtimestamp(signal.timestamp),
                self.METADATA_FIELD: metadata,
                **signal.signal_value.dict(),
            }
            for signal in signal_values
        ]
        return self.db[collection_name].insert_many(inserted_documents)

    def _update_mongo_input_id(self, mongo_input: dict):
        """
        Mongo documents id fields are '_id' while models fields are 'id'. Here id field is
        renamed and other id fields (relation fields) types are converted.
        """
        if self.MODEL_ID_FIELD in mongo_input:
            mongo_input[self.MONGO_ID_FIELD] = ObjectId(
                mongo_input[self.MODEL_ID_FIELD]
            )
            del mongo_input[self.MODEL_ID_FIELD]
        self._fix_input_ids(mongo_input)

    def _update_mongo_output_id(self, mongo_output: dict):
        """
        Mongo documents id fields are '_id' while models fields are 'id'. Here id field is
        renamed and other id fields (relation fields) types are converted.
        """
        if self.MONGO_ID_FIELD in mongo_output:
            mongo_output[self.MODEL_ID_FIELD] = str(mongo_output[self.MONGO_ID_FIELD])
            del mongo_output[self.MONGO_ID_FIELD]
        self._fix_output_ids(mongo_output)

    def _fix_input_ids(self, mongo_query):
        """
        Mongo uses ObjectId in id fields, while models use int/str. This function
        performs conversion on each id field in input query.
        """

        def fix_input_id(field, value):
            if self._field_is_id(field) and value is not None:
                return ObjectId(value)
            return value

        self._mongo_object_deep_iterate(mongo_query, fix_input_id)

    def _fix_output_ids(self, mongo_document):
        """
        Mongo uses ObjectId in id fields, while models use int/str. This function
        performs conversion on each id field in output dict.
        """

        def fix_output_id(field, value):
            if self._field_is_id(field) and value is not None:
                return str(value)
            return value

        self._mongo_object_deep_iterate(mongo_document, fix_output_id)

    @staticmethod
    def _field_is_id(field):
        if type(field) is not str:
            return False
        return field == "id" or field[-3:] in ("_id", ".id")

    def _mongo_object_deep_iterate(self, mongo_object: dict, func):
        """
        Call a function on each primitive value in mongo output document or input query
        dict. Mongo document field values are either primitives, dicts or arrays.
        """
        if type(mongo_object) is not dict:
            return
        for field, value in mongo_object.items():
            if type(value) is dict:
                self._mongo_object_deep_iterate(value, func)
            elif type(value) is list:
                for list_elem in value:
                    self._mongo_object_deep_iterate(list_elem, func)
            else:
                mongo_object[field] = func(field, mongo_object[field])
