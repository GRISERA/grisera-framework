import asyncio
import unittest
import os
from owlready2 import get_ontology
from instance.instance_service import InstanceService
from instance.instance_router import InstanceRouter
from instance.instance_model import MinimalInstanceModelIn,MinimalModelOut
from fastapi import Response

class InstanceServiceTestCase(unittest.TestCase):

    def test_add_instance_model_does_not_exist(self):
        instance_router = InstanceRouter()

        response = Response()
        class_str = "Experiment"
        model_in = MinimalInstanceModelIn(name="test")
        model_id = -100000

        result = asyncio.run(instance_router.add_instance(model_id, class_str, model_in, response))


        self.assertEqual(result.errors,f"Model with id {model_id} not found")

    def test_add_instance_without_error(self):
        instance_router = InstanceRouter()

        response = Response()
        class_str = "Experiment"
        model_in = MinimalInstanceModelIn(name="test")
        model_id = instance_router.instance_service.model_service.create_base_model().id

        asyncio.run(instance_router.add_instance(model_id, class_str, model_in, response))

        os.remove("database" + os.path.sep + str(model_id) + ".owl")

        self.assertEqual(response.status_code, 200)

    def test_add_instance_class_does_not_exist(self):
        instance_router = InstanceRouter()

        response = Response()
        class_str = "Utopia"
        model_in = MinimalInstanceModelIn(name="test")
        model_id = instance_router.instance_service.model_service.create_base_model().id

        result = asyncio.run(instance_router.add_instance(model_id, class_str, model_in, response))

        os.remove("database" + os.path.sep + str(model_id) + ".owl")

        self.assertEqual(result.errors, f"Class named {class_str} not found in Model {model_id}")