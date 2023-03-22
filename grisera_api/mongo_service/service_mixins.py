from abc import ABC, abstractmethod
from typing import Union
from grisera_api.models.not_found_model import NotFoundByIdModel
from mongo_service import mongo_api_service


class ModelClasses:
    """
    Class for holding model classes of mongo service.
    """

    def __init__(self, basic_out_class, out_class):
        self.basic_out_class = basic_out_class
        self.out_class = out_class


class GenericMongoServiceMixin:

    """
    This mixin defines implementation of basic mongo services methods. It requires the sublass to implement:
        model_classes field - instance of ModelClasses object that hold model classes for this service
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

    def get_many_dict(self, query: dict = {}, *args, **kwargs):
        """
        Generic method for sending request to mongo api to get multiple documents. This method doesn't
        return instance of model class.
        Returns:
            Result of request as list of dictionaries.
        """
        basic_out_class = self.model_classes.basic_out_class
        results_dict = mongo_api_service.get_documents(
            basic_out_class, query=query, *args, **kwargs
        )
        return [basic_out_class(**result) for result in results_dict]

    def get_single(self, id: Union[str, int], *args, **kwargs):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of recordings objects
        """
        out_class = self.model_classes.out_class
        result_dict = self.get_traverse(id, 0, "", *args, **kwargs)
        if result_dict is NotFoundByIdModel:
            return result_dict
        return out_class(**result_dict)

    def get_multiple_traverse(
        self, query: dict, depth: int, source: str, *args, **kwargs
    ):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of recordings objects
        """
        out_class = self.model_classes.out_class
        results_dict = mongo_api_service.get_documents(
            out_class, query=query, *args, **kwargs
        )

        for result in results_dict:
            self._add_related_documents(result, depth, source)

        return results_dict

    def get_single_traverse(
        self, id: Union[str, int], depth: int, source: str, *args, **kwargs
    ):
        """
        Generic method for sending request to mongo api to get single document
        Returns:
            Result of request as list of recordings objects
        """
        out_class = self.model_classes.out_class
        result_dict = mongo_api_service.get_document(id, out_class, *args, **kwargs)

        if result_dict is NotFoundByIdModel:
            return result_dict

        self._add_related_documents(result_dict, depth, source)

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
