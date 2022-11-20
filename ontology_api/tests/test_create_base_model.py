from classes.ontology_model_manipulator import OntologyModelManipulator
import asyncio
import unittest
from owlready2 import get_ontology

class CreateBaseModelTestCase(unittest.TestCase):

    def test_create_base_model(self):
        manipulator = OntologyModelManipulator()
        for i in range(0, 10):
            result = manipulator.create_base_model()
            self.assertEqual(result, i)
            self.assertEqual(get_ontology(manipulator.base_iri), manipulator.models.get(i))


