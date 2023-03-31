import unittest
import os
from owlready2 import get_ontology, locstr
from instance.instance_service import InstanceService
from instance.instance_model import MinimalInstanceModelIn, MinimalModelOut

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

    def test_get_instance_model_does_not_exist(self):
        instance_service = InstanceService()
        class_str = "Experiment"
        instance_label = "test"
        model_id = -1
        result = instance_service.get_instance(model_id, class_str, instance_label)
        self.assertEqual(result.errors, f"Model with id {model_id} not found")

    def test_get_instance_without_error(self):
        instance_service = InstanceService()
        model_id = 1
        class_str = "Experiment"
        instance_label = "t"
        instance_id = "test_id"
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        onto_class = onto[class_str]
        instance = onto_class(instance_id)
        instance.label = [locstr(instance_label, lang="en")]
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        result = instance_service.get_instance(model_id, class_str, instance_label)
        self.assertEqual(result.instance_id, instance_id)
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_get_instance_class_does_not_exist(self):
        instance_service = InstanceService()
        model_id = 1
        class_str = "Utopia"
        instance_label = "test"
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        result = instance_service.get_instance(model_id, class_str, instance_label)
        self.assertEqual(result.errors, f"Class named {class_str} not found in Model {model_id}")
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_delete_instance_class_does_not_exist(self):
        instance_service = InstanceService()

        id = instance_service.model_service.create_base_model().id
        class_str = "Utopia"
        model_in = MinimalInstanceModelIn(name="test")
        result = instance_service.delete_instance(id, class_str, model_in)

        os.remove("database" + os.path.sep + str(id) + ".owl")
        self.assertEqual(result, MinimalModelOut(errors=f"Class named {class_str} not found in Model {id}"))

    def test_delete_instance_label_does_not_exist(self):
        instance_service = InstanceService()
        model_id = 1
        class_str = "Experiment"
        instance_label = "tt"
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        result = instance_service.delete_instance(model_id, class_str, instance_label)
        self.assertEqual(result.errors, f"Instance with label {instance_label} not found in Model {model_id}")
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_delete_instance_model_does_not_exist(self):
        instance_service = InstanceService()
        class_str = "Experiment"
        instance_label = "test"
        model_id = -1
        result = instance_service.delete_instance(model_id, class_str, instance_label)
        self.assertEqual(result.errors, f"Model with id {model_id} not found")

    def test_delete_instance_without_error(self):
        instance_service = InstanceService()
        model_id = 1
        class_str = "Experiment"
        instance_label = "t"
        instance_id = "test_id"
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        onto_class = onto[class_str]
        instance = onto_class(instance_id)
        instance.label = [locstr(instance_label, lang="en")]
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()

        result = instance_service.delete_instance(model_id, class_str, instance_label)

        self.assertEqual(result.instance_id, instance_id)
        os.remove("database" + os.path.sep + f"{model_id}.owl")