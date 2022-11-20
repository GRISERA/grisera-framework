import unittest
from owlready2 import get_ontology
import os
from classes.ontology_model_manipulator import OntologyModelManipulator

class TestGetGetOwlFromModel(unittest.TestCase):
    def test_get_owl_from_model_identical_ontologies(self):
        manipulator = OntologyModelManipulator()
        manipulator.models[1] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        manipulator.models[2] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        f1 = manipulator.get_owl_from_model(1,'tests/tmp_owl')
        f2 = manipulator.get_owl_from_model(2,'tests/tmp_owl')
        content1 = f1.read()
        content2 = f2.read()
        f1.close()
        f2.close()
        os.remove(f1.name)
        os.remove(f2.name)
        self.assertEqual(content1, content2)

    def test_get_owl_from_model_incorrect_path(self):
        manipulator = OntologyModelManipulator()
        manipulator.models[1] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        with self.assertRaises(Exception) as context:
            manipulator.get_owl_from_model(1, path="E:/Users")
        self.assertTrue("Incorrect path", context.exception)
