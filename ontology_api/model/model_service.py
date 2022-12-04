from owlready2 import get_ontology

from instance.instance_model import MinimalInstanceModelIn
from model.model_model import ModelOut
from fastapi import UploadFile
import os

class ModelService:
    """
    Object to handle logic of models requests

    Attributes:
        models (Dictionary): database mock
    """
    models = dict()
    def __find_model_by_id(self, model_id):
        return self.models.get(model_id)

    def __add_model(self,model_id,model):
        self.models[model_id] = model

    def __check_model_exist(self, model_id):
        return model_id in self.models

    def __generate_id(self):
        for model_id in range(len(self.models), -1, -1):
            if model_id not in self.models.keys():
                return model_id

    def save_model(self, file: UploadFile) -> ModelOut:
        if not file.filename.endswith('.owl'):
            return ModelOut(errors="Wrong extension of file")
        with open(file.filename, 'wb') as new_file:
            content = file.file.read()
            new_file.write(content)
            new_file.close()
        try:
            response = self.create_model(file.filename)
        except Exception:
            result = ModelOut(errors="Cannot create model")
        else:
            result = ModelOut(id=response)
        return result

    def create_model(self, file_path) -> int:
        try:
            model = get_ontology(file_path).load()
        except OSError:
            raise Exception("Cannot open file")
        model_id = self.__generate_id()
        self.__add_model(model_id, model)
        return model_id

    def create_base_model(self) -> ModelOut:
        base_iri = "https://road.affectivese.org/documentation/owlAC.owl"
        try:
            response = self.create_model(base_iri)
        except Exception:
            result = ModelOut(errors="Cannot create model")
        else:
            result = ModelOut(id=response)
        return result

    def save_model_as_owl(self, model, model_id, path=None):
        if model is None:
            return None
        if path is None:
            full_path = model.name + str(model_id) + ".owl"
        else:
            full_path = path + os.path.sep + model.name + str(model_id) + ".owl"
        try:
            model.save(file=full_path, format="rdfxml")
        except OSError:
            return None
        return full_path

    def get_owl_from_model(self, model_id, path=None):
        model = self.__find_model_by_id(model_id)
        return self.save_model_as_owl(model, model_id, path)

    def add_instance(self, class_id, model_id, model_in: MinimalInstanceModelIn):
        if not self.__check_model_exist(model_id):
            return {"error": "Model with id " + str(model_id) + " not found"}

        model = self.__find_model_by_id(model_id)
        classes = list(model.classes())

        if len(classes) <= abs(class_id):
            return {"error": "Class with id " + str(class_id) + " not found in Model " + str(model_id)}

        classes[model_id](model_in.name)