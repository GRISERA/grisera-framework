import unittest
import os
from owlready2 import get_ontology
from model.model_service import ModelService
from fastapi import UploadFile

def save_test_model():
    onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
    path = "tests" + os.path.sep + "tmp_owl" + os.path.sep + "test1.owl"
    onto.save(file=path, format="rdfxml")
    return path

class ModelServiceTestCase(unittest.TestCase):

    def test_create_base_model_without_error(self):
        model_service = ModelService()
        result1 = model_service.create_base_model()
        result2 = model_service.create_base_model()
        os.remove("database" + os.path.sep + "1.owl")
        os.remove("database" + os.path.sep + "2.owl")
        self.assertEqual(result1.id, 1)
        self.assertEqual(result2.id, 2)

    def test_save_model_without_error(self):
        model_service = ModelService()
        new_file = open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.owl", "x")
        new_file.write("<rdf:RDF xml:base=\"http://www.semanticweb.org/GRISERA/contextualOntology\"><owl:Ontology rdf:about=\"http://www.semanticweb.org/GRISERA/contextualOntology\"/></rdf:RDF> ")
        new_file.close()
        with open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.owl", "rb") as f:
            file = UploadFile('testfile.owl', f)
            result = model_service.save_model(file)
        os.remove("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.owl")
        os.remove("database" + os.path.sep + "1.owl")
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
