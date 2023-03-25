from abc import ABC, abstractmethod
from typing import Union
from models.not_found_model import NotFoundByIdModel
from mongo_service import mongo_api_service


class GenericMongoServiceMixin:

    """
    This mixin defines implementation of basic mongo services methods. It requires the sublass to implement:
        model_out_class field - out model class of services model
        _add_related_documents method - method for adding related documents to result when traversing models
    """

    def create(self, object_in):
        """
        Generic method for sending request to mongo api to create new document

        Args:
            object_in: Object based on which document is to be created

        Returns:
            Result of request as data object
        """
        created_document_id = mongo_api_service.create_document(object_in)

        return self.get_single(created_document_id)

    def get_multiple(
        self, query: dict = {}, depth: int = 0, source: str = "", *args, **kwargs
    ):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of dictionaries
        """
        out_class = self.model_out_class
        results_dict = mongo_api_service.get_documents(
            out_class, query=query, *args, **kwargs
        )

        for result in results_dict:
            self._add_related_documents(result, depth, source)

        return results_dict

    def get_single_dict(
        self, id: Union[str, int], depth: int = 0, source: str = "", *args, **kwargs
    ):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of recordings objects
        """
        out_class = self.model_out_class
        result_dict = mongo_api_service.get_document(id, out_class, *args, **kwargs)

        if result_dict is NotFoundByIdModel:
            return result_dict

        self._add_related_documents(result_dict, depth, source)

        return result_dict

    def get_single(
        self, id: Union[str, int], depth: int = 0, source: str = "", *args, **kwargs
    ):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of recordings objects
        """
        out_class = self.model_out_class
        result_dict = self.get_single_dict(id, depth, source, *args, **kwargs)
        return out_class(**result_dict)

    def update(self, id: Union[str, int], updated_object):
        """
        Generic method for sending request to mongo api to update single document
        Returns:
            Updated object
        """
        get_response = self.get_single(id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        mongo_api_service.update_document(id, updated_object)

        return self.get_single(id)

    def delete(self, id: Union[str, int]):
        """
        Generic method for delete request to mongo api
        Returns:
            Deleted object
        """
        existing_document = self.get_single(id)

        if existing_document is None:
            return NotFoundByIdModel(
                id=id,
                errors={"errors": "document with such id not found"},
            )

        mongo_api_service.delete_document(existing_document)
        return existing_document
