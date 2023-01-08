import unittest
import os
from owlready2 import get_ontology
from model.model_service import ModelService
from instance.instance_model import MinimalInstanceModelIn
from fastapi import UploadFile

def save_test_model():
    onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
    path = "tests" + os.path.sep + "tmp_owl" + os.path.sep + "test1.owl"
    onto.save(file=path, format="rdfxml")
    return path

class ModelServiceTestCase(unittest.TestCase):
    def test_get_owl_from_model_without_error(self):
        model_service = ModelService()
        model_service.models[1] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        path_1 = save_test_model()
        path_2 = model_service.get_owl_from_model(model_id=1, path="tests" + os.path.sep + "tmp_owl")
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
        path_1 = "tests" + os.path.sep + "tmp_owl" + os.path.sep + "test1.owl"
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

    def test_create_base_model_without_error(self):
        model_service = ModelService()
        result = model_service.create_base_model()
        self.assertEqual(result.id,6)

    def test_create_model_without_error(self):
        model_service = ModelService()
        new_file = open("testfile.owl", "x")
        new_file.write("<rdf:RDF xml:base=\"http://www.semanticweb.org/GRISERA/contextualOntology\"><owl:Ontology rdf:about=\"http://www.semanticweb.org/GRISERA/contextualOntology\"/></rdf:RDF> ")
        new_file.close()
        result = model_service.create_model("testfile.owl")
        os.remove("testfile.owl")
        self.assertEqual(result,7)

    def test_create_model_with_error(self):
        model_service = ModelService()
        with self.assertRaises(Exception) as context:
            model_service.create_model("interestingnameoffile")
        self.assertTrue("Cannot open file", context.exception)

    def test_save_model_without_error(self):
        model_service = ModelService()
        new_file = open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.owl", "x")
        new_file.write("<rdf:RDF xml:base=\"http://www.semanticweb.org/GRISERA/contextualOntology\"><owl:Ontology rdf:about=\"http://www.semanticweb.org/GRISERA/contextualOntology\"/></rdf:RDF> ")
        new_file.close()
        with open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.owl", "rb") as f:
            file = UploadFile('testfile.owl', f)
            result = model_service.save_model(file)
        os.remove("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.owl")
        os.remove("testfile.owl")
        self.assertNotEqual(result.id, None)

    def test_save_model_with_error_wrong_extension(self):
        model_service = ModelService()
        new_file = open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.txt", "x")
        new_file.write("content")
        new_file.close()
        with open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.txt", "rb") as f:
            file = UploadFile('testfile.txt', f)
            result = model_service.save_model(file)
        os.remove("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.txt")
        self.assertEqual(result.errors, "Wrong extension of file")

    def test_add_instance_happy_path(self):
        model_service = ModelService()
        result1 = model_service.create_base_model()
        model_in = MinimalInstanceModelIn()
        model_in.name = "test"
        result2 = model_service.add_instance(result1.id, "Channel", model_in)
        self.assertEqual(result2,None)

    def test_add_instance_model_not_found(self):
        model_service = ModelService()
        model_in = MinimalInstanceModelIn()
        model_in.name = "test"
        result2 = model_service.add_instance(-1, "Channel", model_in)
        self.assertEqual(result2["error"], "Model with id -1 not found")

    def test_add_instance_class_not_found(self):
        model_service = ModelService()
        result1 = model_service.create_base_model()
        model_in = MinimalInstanceModelIn()
        model_in.name = "test"
        class_name = "Utopia"
        result2 = model_service.add_instance(result1.id, class_name, model_in)
        self.assertEqual(result2["error"], "Class named " + str(class_name) + " not found in Model " + str(result1.id))
