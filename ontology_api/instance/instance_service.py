from owlready2 import get_ontology,locstr
from model.model_model import ModelOut
from instance.instance_model import MinimalInstanceModelIn
from instance.instance_model import MinimalModelOut as InstanceModelOut
from model.model_service import ModelService
from fastapi import UploadFile
import os


class InstanceService:

    def __init__(self):
        self.model_service = ModelService()

    def add_instance(self, model_id, class_name: str, model_in: MinimalInstanceModelIn):
        """
                Create instance of given class in given model
        """
        onto = self.model_service.load_ontology(model_id)

        if onto is None:
            return InstanceModelOut(errors="Model with id " + str(model_id) + " not found")

        owl_class = onto[class_name]
        if owl_class is None:
            return InstanceModelOut(errors="Class named " + str(class_name) + " not found in Model " + str(model_id))

        instance = owl_class(model_in.name)
        instance.label = [locstr(model_in.name, lang = "en")]
        model_out = self.model_service.update_ontology(model_id, onto)

        if model_out.errors is not None:
            return InstanceModelOut(errors=model_out.errors)
        else:
            return InstanceModelOut(label=model_in.name)