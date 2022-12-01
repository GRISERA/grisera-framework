from typing import List
import owlready2


f = open("dfghjk.txt","w")
f.write("sdfghjhgfghj!")
f.close()

class ModelService:
    """
    Object to handle logic of models requests

    Attributes:
        models (Dictionary): database mock
    """
    models = dict()
    models[1] = owlready2.get_ontology("http://www.semanticweb.org/GRISERA/contextualOntology")
    
    
    

    def __find_model_by_id(self, model_id):
        return self.models[model_id]

    def __add_model(self,model_id,model):
        self.models[model_id] = model

    def __check_model_exist(self, model_id):
        return id in self.models

    def __generate_id(self):
        for model_id in range(len(self.models), -1, -1):
            if model_id not in self.models.keys():
                return model_id

    def create_model(self,file_path ) -> int:
        pass

    def create_base_model(self):
        return self.create_model(self.base_iri)

    def add_instance(self,instance, class_name, model_id):
        pass

    def save_model_as_owl(self,model,model_id, path="tmp_owl"):
        full_path = path + "/" + model.name + str(model_id) + ".owl"
        try:
            model.save(file=full_path, format = "rdfxml")
        except OSError:
            return None
        return full_path

    def get_owl_from_model(self,model_id, path="tmp_owl"):
        model = self.__find_model_by_id(model_id)
        return self.save_model_as_owl(model, model_id, path)
        
