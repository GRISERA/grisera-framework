from functions.functions import models
from functions.functions import create_base_model
from functions.functions import base_iri
import asyncio
import unittest
from owlready2 import get_ontology

class CreateBaseModelTestCase(unittest.TestCase):

    def test_create_base_model(self):
        models.clear()
        for i in range(0, 10):
            result = create_base_model()
            self.assertEqual(result, i)
            self.assertEqual(get_ontology(base_iri), models.get(i))


