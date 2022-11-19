import asyncio
import unittest
import unittest.mock as mock

from functions.functions import create_model
from functions.functions import models


class CreateModelTestCase(unittest.TestCase):


    def test_create_model_without_error(self):
        my_path = "tests\\test_owl\\owlAC_testParticipant.owl"
        models.clear()

        result = create_model(my_path)

        self.assertEqual(result , 0)
        models.clear()


    def test_create_model_with_error(self):
        my_path = "xd.owl"
        with self.assertRaises(Exception) as context:
            result = create_model(my_path)
        self.assertTrue("Cannot open file", context.exception)
        models.clear()


    def test_create_model_without_error_add_more(self):
        my_path = "tests\\test_owl\\owlAC_testParticipant.owl"
        models.clear()
        create_model(my_path)
        create_model(my_path)
        create_model(my_path)
        models.pop(2)

        result = create_model(my_path)

        self.assertEqual(result, 2)
        models.clear()