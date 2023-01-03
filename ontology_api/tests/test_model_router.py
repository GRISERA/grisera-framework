import asyncio
import unittest
import os
from fastapi import Response, UploadFile
from owlready2 import get_ontology
from model.model_router import ModelRouter

class ModelRouterTestCase(unittest.TestCase):

    def test_get_owl_without_error(self):
        model_router = ModelRouter()
        response = Response()
        model = get_ontology("http://www.semanticweb.org/GRISERA/contextualOntology")
        model.save(file="database" + os.path.sep + "0.owl", format="rdfxml")
        result = asyncio.run(model_router.get_owl(0, response))
        os.remove("database" + os.path.sep + "0.owl")
        self.assertEqual(response.status_code, 200)

    def test_get_owl_with_error(self):
        model_router = ModelRouter()
        response = Response()
        result = asyncio.run(model_router.get_owl(1000, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result, {"error": "File not found!"})

    def test_create_model_with_file_without_error(self):
        model_router = ModelRouter()
        response = Response()
        new_file = open("testfile.owl", "x")
        new_file.write("<rdf:RDF xml:base=\"http://www.semanticweb.org/GRISERA/contextualOntology\"><owl:Ontology rdf:about=\"http://www.semanticweb.org/GRISERA/contextualOntology\"/></rdf:RDF> ")
        new_file.close()
        file = UploadFile('testfile.owl')
        result = asyncio.run(model_router.create_model(response, file))
        os.remove("testfile.owl")
        os.remove("database" + os.path.sep + "1.owl")
        self.assertEqual(response.status_code, 200)

    def test_create_model_with_file_with_error(self):
        model_router = ModelRouter()
        response = Response()
        new_file = open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.txt", "x")
        new_file.write("Rose is a rose is a rose is a rose")
        new_file.close()
        with open("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.txt", "rb") as f:
            file = UploadFile('testfile.txt',f)
            result = asyncio.run(model_router.create_model(response, file))
        os.remove("tests" + os.path.sep + "tmp_owl" + os.path.sep + "testfile.txt")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result.errors, "Wrong extension of file")
