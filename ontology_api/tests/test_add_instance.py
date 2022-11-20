import unittest
import unittest.mock as mock
from owlready2 import get_ontology, Thing
from classes.ontology_model_manipulator import OntologyModelManipulator


class AddInstanceTest(unittest.TestCase):

    def test_add_instance_happy_path(self):
        manipulator = OntologyModelManipulator()
        onto = get_ontology(manipulator.base_iri)
        with onto:
            class C(Thing):
                pass
        manipulator.models[0]=onto
        self.assertEqual(manipulator.add_instance("c",C,0),None)

    def test_add_instance_model_doesnt_exist(self):
        manipulator = OntologyModelManipulator()
        manipulator.models.clear()
        onto = get_ontology(manipulator.base_iri)
        with onto:
            class C(Thing):
                pass
        with self.assertRaises(Exception) as context:
            manipulator.add_instance("c",C,0)
        self.assertTrue("Model with id 0 doesn't exist", context.exception)

    def test_add_instance_class_doesnt_exist(self):
        manipulator = OntologyModelManipulator()
        onto = get_ontology(manipulator.base_iri)
        manipulator.models[0] = onto
        class X(Thing):
            pass
        self.assertRaises(Exception, manipulator.add_instance("c", X, 0))




