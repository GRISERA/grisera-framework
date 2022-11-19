from owlready2 import *

# TODO jakaś śmieszna struktra zawierajaca wygenerowane modele i ich id, czyli pewnie jakaś mapa/dictionary
models = dict()

# model podstawowy
base_iri = "http://www.semanticweb.org/GRISERA/contextualOntology"


def create_model(filePath):
    model = get_ontology('file://' + filePath).load()
    # TODO zapisać model i id w naszej śmiesznej strukturze
    model_id = 0
    return model_id


def create_base_model():
    # TODO trzeba jakos zmienić bo tu bierzemy po iri a nie file. Najłatwiej zduplikować kod create_model
    #      ale może warto to jakoś sprytniej zrobić
    return create_model(base_iri)


def add_instance(instance, class_name, model_id):
    if model_id not in models:
        raise Exception("Model with id " + str(model_id) + " doesn't exist")
    class_name(instance, namespace=models[model_id])
    return


def get_model(model_id):
    # TODO znaleźć model o danym id, zapisać go do pliku OWL i zwrocic ten plik (w jakiej formie? nie wiem).
    return


# Zwraca model ontologii z naszej śmiesznej struktury i go zwraca
def find_model_by_id(model_id):
    return

# TODO TESTY!!!
