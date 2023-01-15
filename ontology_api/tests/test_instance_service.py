import unittest
import os
from owlready2 import get_ontology
from instance.instance_service import InstanceService
from instance.instance_model import MinimalInstanceModelIn,MinimalModelOut

class InstanceServiceTestCase(unittest.TestCase):

    def test_add_instance_model_does_not_exist(self):
        instance_service = InstanceService()

        class_str = "Experiment"
        model_in = MinimalInstanceModelIn(name="test")
        er_model_id = -100000

        result = instance_service.add_instance(er_model_id, class_str,model_in)
        self.assertEqual(result, MinimalModelOut(errors=f"Model with id {er_model_id} not found"))

    def test_add_instance_without_error(self):
        instance_service = InstanceService()
        id = instance_service.model_service.create_base_model().id
        class_str = "Experiment"
        model_in = MinimalInstanceModelIn(name="test")
        result = instance_service.add_instance(id, class_str, model_in)
        os.remove("database" + os.path.sep + str(id) + ".owl")
        self.assertEqual(result, MinimalModelOut(label=model_in.name))

    def test_add_instance_class_does_not_exist(self):
        instance_service = InstanceService()

        id = instance_service.model_service.create_base_model().id
        class_str = "Utopia"
        model_in = MinimalInstanceModelIn(name="test")
        result = instance_service.add_instance(id, class_str, model_in)

        os.remove("database" + os.path.sep + str(id) + ".owl")
        self.assertEqual(result, MinimalModelOut(errors=f"Class named {class_str} not found in Model {id}"))