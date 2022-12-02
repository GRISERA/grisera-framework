import asyncio
import unittest
import unittest.mock as mock
import os
from fastapi import Response, BackgroundTasks
from owlready2 import get_ontology
from model.model_router import ModelRouter

class ModelRouterTestCase(unittest.TestCase):

    def test_get_owl_without_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        model_router.model_service.models[1] = get_ontology("http://www.semanticweb.org/GRISERA/contextualOntology")
        result = asyncio.run(model_router.get_owl(1, response, background_tasks))
        os.remove("tmp_owl/contextualOntology1.owl")
        self.assertEqual(response.status_code, 200)

    def test_get_owl_with_error(self):
        model_router = ModelRouter()
        response = Response()
        background_tasks = BackgroundTasks()
        result = asyncio.run(model_router.get_owl(1, response,background_tasks))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result, {"error": "File not found!"})
