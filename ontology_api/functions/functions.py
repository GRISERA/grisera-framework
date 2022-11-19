from owlready2 import *


models = dict()

# model podstawowy
base_iri = "http://www.semanticweb.org/GRISERA/contextualOntology"

def generate_id():
    for id in range(len(models), -1, -1):
        if id in models.keys():
            pass
        else:
            return id


def create_model(file_path) -> int:
    try:
        model = get_ontology(file_path).load()
    except OSError:
        raise Exception("Cannot open file")
    model_id = generate_id()
    models[model_id] = model
    return model_id


def create_base_model():
    model = get_ontology(base_iri)
    model_id = generate_id()
    models[model_id] = model
    return model_id

def add_instance(instance, class_name, model_id):
    # TODO znaleźć model o danym id, wrzucić tam instancję
    return

def get_owl_from_model(model_id, path="tmp_owl"):
    model = find_model_by_id(model_id)
    try:
        model.save(path + "/" + model.name + str(model_id) + ".owl")
    except OSError:
        raise Exception("Incorrect path")
    try:
        return open(path + "/" + model.name + str(model_id) + ".owl", "r")
    except OSError:
        return Exception("Could not find model")

# Zwraca model ontologii z naszej śmiesznej struktury i go zwraca
def find_model_by_id(model_id):
    return models[model_id]

