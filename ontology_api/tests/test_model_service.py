import unittest
import os
from owlready2 import get_ontology
from model.model_service import ModelService

def save_test_model():
    onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
    path = "tests/tmp_owl/test1.owl"
    onto.save(file=path, format="rdfxml")
    return path

class ModelServiceTestCase(unittest.TestCase):
    def test_get_owl_from_model_without_error(self):
        model_service = ModelService()
        model_service.models[1] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        path_1 = save_test_model()
        path_2 = model_service.get_owl_from_model(model_id=1, path="tests/tmp_owl")
        file_1 = open(path_1)
        file_2 = open(path_2)
        content_1 = file_1.read()
        content_2 = file_2.read()
        file_1.close()
        file_2.close()
        os.remove(file_1.name)
        os.remove(file_2.name)
        model_service.models.pop(1)
        self.assertEqual(content_1, content_2)

    def test_get_owl_from_model_without_existing_model(self):
        model_service = ModelService()
        result = model_service.get_owl_from_model(1)
        self.assertIsNone(result)

    def test_save_model_as_owl_without_error(self):
        model_service = ModelService()
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        path_1 = "tests/tmp_owl/test1.owl"
        path_2 = model_service.save_model_as_owl(onto, 1)
        onto.save(path_1)
        file_1 = open(path_1)
        file_2 = open(path_2)
        content_1 = file_1.read()
        content_2 = file_2.read()
        file_1.close()
        file_2.close()
        os.remove(file_1.name)
        os.remove(file_2.name)
        self.assertEqual(content_1, content_2)

    def test_save_model_as_owl_with_error(self):
        model_service = ModelService()
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        path = "this/doesnt/exist"
        self.assertIsNone(model_service.save_model_as_owl(onto, 1, path=path))
