import asyncio
import unittest
import unittest.mock as mock

from functions.functions import create_model
from functions.functions import models


class CreateModelTestCase(unittest.TestCase):

    @mock.patch('functions.functions','create_model')
    def test_create_model_without_error(self):
        my_path = "tests\\owlAC_testParticipant.owl"
        models.clear()

        result = create_model(my_path)

        self.assertEqual(result , 0)

    @mock.patch('functions.functions', 'create_model')
    def test_create_model_with_error(self):
        my_path = "D:\\xd.owl"

        result = create_model(my_path)

        self.assertEqual(result, "Cannot open file")

    @mock.patch('functions.functions', 'create_model')
    def test_create_model_without_error_add_more(self):
        my_path = "D:\\owlAC_testParticipant.owl"
        models.clear()
        create_model(my_path)
        create_model(my_path)
        create_model(my_path)
        create_model(my_path)

        result = create_model(my_path)

        self.assertEqual(result, 4)