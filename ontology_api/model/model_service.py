from owlready2 import get_ontology
from model.model_model import ModelOut
from fastapi import UploadFile
import os

class ModelService:
    """
    Object to handle logic of models requests
    """

    def __find_model_by_id(self, model_id):
        return get_ontology("database" + os.path.sep + str(model_id) + ".owl").load()

    def __add_model(self,model_id,model):
        model.save(file="database" + os.path.sep + str(model_id) + ".owl", format="rdfxml")

    def __check_model_exist(self, model_id):
        return os.path.isfile("database" + os.path.sep + str(model_id) + ".owl")

    def __generate_id(self):
        files = os.listdir('database')
        files.sort(reverse=True)
        for model_id in range(len(files), -1, -1):
            new_file_name = str(model_id) + ".owl"
            if new_file_name not in files:
                return model_id

    def save_model(self, file: UploadFile) -> ModelOut:
        if not file.filename.endswith('.owl'):
            return ModelOut(errors="Wrong extension of file")
        new_id = self.__generate_id()
        try:
            with open("database" + os.path.sep + str(new_id) + ".owl", 'wb') as new_file:
                content = file.file.read()
                new_file.write(content)
        except IOError:
            result = ModelOut(errors="Cannot create model")
        else:
            result = ModelOut(id=new_id)
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

    def get_owl_from_model(self, model_id, path=None):
        if self.__check_model_exist(model_id):
            return "database" + os.path.sep + str(model_id) + ".owl"
        return None