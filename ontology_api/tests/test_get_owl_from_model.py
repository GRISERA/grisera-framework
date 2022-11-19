import unittest
from owlready2 import get_ontology
import os
from functions.functions import models, get_owl_from_model

class TestGetGetOwlFromModel(unittest.TestCase):
    def test_get_owl_from_model_identical_ontologies(self):
        models.clear()
        models[1] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        models[2] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        f1 = get_owl_from_model(1,'tests/tmp_owl')
        f2 = get_owl_from_model(2,'tests/tmp_owl')
        content1 = f1.read()
        content2 = f2.read()
        f1.close()
        f2.close()
        os.remove(f1.name)
        os.remove(f2.name)
        models.clear()
        self.assertEqual(content1, content2)

    def test_get_owl_from_model_incorrect_path(self):
        models.clear()
        models[1] = get_ontology("https://road.affectivese.org/documentation/owlAC.owl")
        with self.assertRaises(Exception) as context:
            get_owl_from_model(1, path="E:/Users")
        self.assertTrue("Incorrect path", context.exception)
        models.clear()
