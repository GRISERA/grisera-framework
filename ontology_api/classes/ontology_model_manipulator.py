from owlready2 import get_ontology


class OntologyModelManipulator:

    def __init__(self):
        # Structure carrying models for ontology
        self.models = dict()
        # base model
        self.base_iri = "http://www.semanticweb.org/GRISERA/contextualOntology"

    # helper function for create_model
    # generates unique id for an ontology model
    def generate_id(self):
        for id in range(len(self.models), -1, -1):
            if id in self.models.keys():
                pass
            else:
                return id

    # loads an owl ontology to a model
    # params file_path: owl file path or iri (str)
    # return id of new model (int)
    def create_model(self,file_path ) -> int:
        try:
            model = get_ontology(file_path).load()
        except OSError:
            raise Exception("Cannot open file")
        model_id = self.generate_id()
        self.models[model_id] = model
        return model_id

    # loads the ROAD core ontology
    # return id of new model (int)
    def create_base_model(self):
        return self.create_model(self.base_iri)

    # adds a new instance of a class to an ontology model
    # params instance: name of the instance (str)
    #        class_name: class of the instance to be added (class)
    #        model_id: ID of the ontology model (int)
    def add_instance(self,instance, class_name, model_id):
        if model_id not in self.models:
            raise Exception("Model with id " + str(model_id) + " doesn't exist")
        class_name(instance, namespace=self.models[model_id])
        return

    # helper function for get_owl_from_model
    # saves model as owl file
    # params model: ontology model
    #        model_id: id of model to be saved (int)
    #        path: directory where the file will be saved (str)
    def save_model_as_owl(self,model,model_id, path="tmp_owl"):
        try:
            model.save(path + "/" + model.name + str(model_id) + ".owl")
        except OSError:
            raise Exception("Incorrect path")

    # saves an ontology model as owl file and returns it
    # params model_id: id of model to be saved (id)
    #        path: directory where the file will be saved (str)
    # return owl file object
    def get_owl_from_model(self,model_id, path="tmp_owl"):
        model = self.find_model_by_id(model_id)
        self.save_model_as_owl(model,model_id,path)
        try:
            return open(path + "/" + model.name + str(model_id) + ".owl", "r")
        except OSError:
            raise Exception("Could not find model")

    # gets a model with the gived id
    def find_model_by_id(self,model_id):
        return self.models[model_id]

