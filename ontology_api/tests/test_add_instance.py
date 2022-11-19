import unittest
import unittest.mock as mock
from owlready2 import get_ontology, Thing
from functions.functions import base_iri, add_instance, models


class AddInstanceTest(unittest.TestCase):

    def test_add_instance_happy_path(self):
        onto = get_ontology(base_iri)
        with onto:
            class C(Thing):
                pass
        models[0]=onto
        self.assertEqual(add_instance("c",C,0),None)

    def test_add_instance_model_doesnt_exist(self):
        onto = get_ontology(base_iri)
        with onto:
            class C(Thing):
                pass
        self.assertRaises(Exception,add_instance("c",C,0))

    def test_add_instance_class_doesnt_exist(self):
        onto = get_ontology(base_iri)
        models[0] = onto
        class X(Thing):
            pass
        self.assertRaises(Exception, add_instance("c", X, 0))




