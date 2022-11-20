import unittest

from classes.ontology_model_manipulator import OntologyModelManipulator

class CreateModelTestCase(unittest.TestCase):


    def test_create_model_without_error(self):
        manipulator = OntologyModelManipulator()
        my_path = "tests\\test_owl\\owlAC_testParticipant.owl"

        result = manipulator.create_model(my_path)

        self.assertEqual(result , 0)


    def test_create_model_with_error(self):
        manipulator = OntologyModelManipulator()
        my_path = "xd.owl"
        with self.assertRaises(Exception) as context:
            result = manipulator.create_model(my_path)
        self.assertTrue("Cannot open file", context.exception)


    def test_create_model_without_error_add_more(self):
        manipulator = OntologyModelManipulator()
        my_path = "tests\\test_owl\\owlAC_testParticipant.owl"
        manipulator.create_model(my_path)
        manipulator.create_model(my_path)
        manipulator.create_model(my_path)
        manipulator.models.pop(2)

        result = manipulator.create_model(my_path)

        self.assertEqual(result, 2)