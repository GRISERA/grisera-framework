import asyncio
import unittest
import unittest.mock as mock
import os
from fastapi import Response, BackgroundTasks, UploadFile
from owlready2 import get_ontology

from instance.instance_model import MinimalInstanceModelIn
from model.model_router import ModelRouter

class ModelRouterTestCase(unittest.TestCase):

    def test_get_owl_without_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        model_router.model_service.models[1] = get_ontology("http://www.semanticweb.org/GRISERA/contextualOntology")
        result = asyncio.run(model_router.get_owl(1, response, background_tasks))
        #os.remove("tmp_owl/contextualOntology1.owl")
        self.assertEqual(response.status_code, 200)

    def test_get_owl_with_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        result = asyncio.run(model_router.get_owl(1000, response,background_tasks))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result, {"error": "File not found!"})

    def test_create_model_with_file_without_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        new_file = open("testfile.owl", "x")
        new_file.write("<rdf:RDF xml:base=\"http://www.semanticweb.org/GRISERA/contextualOntology\"><owl:Ontology rdf:about=\"http://www.semanticweb.org/GRISERA/contextualOntology\"/></rdf:RDF> ")
        new_file.close()
        file = UploadFile('testfile.owl')
        result = asyncio.run(model_router.create_model(response, background_tasks, file))
        os.remove("testfile.owl")
        self.assertEqual(response.status_code, 200)

    def test_create_model_without_file_without_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        result = asyncio.run(model_router.create_model(response, background_tasks))
        self.assertEqual(response.status_code, 200)

    def test_create_model_with_file_with_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        new_file = open("tests/tmp_owl/testfile.txt", "x")
        new_file.write("Rose is a rose is a rose is a rose")
        new_file.close()
        with open("tests/tmp_owl/testfile.txt", "rb") as f:
            file = UploadFile('testfile.txt',f)
            result = asyncio.run(model_router.create_model(response, background_tasks, file))
        os.remove("tests/tmp_owl/testfile.txt")
        #os.remove("testfile.txt")
        self.assertEqual(response.status_code, 422)

    def test_add_instance_happy_path(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        result1 = model_router.model_service.create_base_model()
        model_in = MinimalInstanceModelIn()
        model_in.name = "test"
        result = asyncio.run(model_router.add_instance(result1.id,0,model_in,response))
        self.assertEqual(response.status_code, 200)

    def test_add_instance_model_not_found(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        model_in = MinimalInstanceModelIn()
        model_in.name = "test"
        result = asyncio.run(model_router.add_instance(-1, 0, model_in, response))
        self.assertEqual(response.status_code, 422)

    def test_add_instance_class_not_found(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        result1 = model_router.model_service.create_base_model()
        model_in = MinimalInstanceModelIn()
        model_in.name = "test"
        result = asyncio.run(model_router.add_instance(result1.id, 1000000000000000, model_in, response))
        self.assertEqual(response.status_code, 422)




