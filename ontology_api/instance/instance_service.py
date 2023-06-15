from owlready2 import get_ontology, locstr, destroy_entity, ObjectPropertyClass, DataPropertyClass
from model.model_model import ModelOut
from instance.instance_model import MinimalInstanceModelIn, FullInstanceModelOut, InstancesModelOut
from instance.instance_model import MinimalModelOut as InstanceModelOut
from model.model_service import ModelService
import os


class InstanceService:

    def __init__(self):
        self.model_service = ModelService()

    def add_instance(self, model_id, class_name: str, model_in: MinimalInstanceModelIn):
        """
                Create instance of given class in given model
        """
        onto = self.model_service.load_ontology(model_id)

        if onto is None:
            return InstanceModelOut(errors="Model with id " + str(model_id) + " not found")

        owl_class = onto[class_name]
        if owl_class is None:
            onto.destroy()
            return InstanceModelOut(errors="Class named " + str(class_name) + " not found in Model " + str(model_id))
        
        instance = owl_class(model_in.name)
        instance.label = [locstr(model_in.name, lang = "en")]
        model_out = self.model_service.update_ontology(model_id, onto)

        if model_out.errors is not None:
            return InstanceModelOut(errors=model_out.errors)
        else:
            return InstanceModelOut(label=model_in.name)

    def get_instance(self, model_id: int, class_name: str, instance_label: str):
        """
                Return instance with a given label
        """
        onto = self.model_service.load_ontology(model_id)
        if onto is None:
            return InstanceModelOut(errors="Model with id " + str(model_id) + " not found")
        owl_class = onto[class_name]
        if owl_class is None:
            onto.destroy()
            return InstanceModelOut(errors="Class named " + str(class_name) + " not found in Model " + str(model_id))
        for i in owl_class.instances():
            if len(i.label) > 0 and i.label[0] == instance_label:
                instance_id = i.name
                onto.destroy()
                return FullInstanceModelOut(instance_id=instance_id, label=instance_label)
        onto.destroy()
        return InstanceModelOut(
            errors="Instance with label " + str(instance_label) + " not found in Model " + str(model_id))

    def get_instances(self, model_id: int, class_name: str):
        """
            Return all instances of a given class
        """
        onto = self.model_service.load_ontology(model_id)
        if onto is None:
            return InstanceModelOut(errors="Model with id " + str(model_id) + " not found")
        owl_class = onto[class_name]
        if owl_class is None:
            onto.destroy()
            return InstanceModelOut(errors="Class named " + str(class_name) + " not found in Model " + str(model_id))
        instance_names = onto.search(type=owl_class)
        instances = []
        for instance in instance_names:
            instance_name = instance.name
            instance_roles = []
            for prop in instance.get_properties():
                for value in prop[instance]:
                    if isinstance(prop, ObjectPropertyClass):
                        instance_roles.append({'role': prop.name, 'value': value.name})
                    elif isinstance(prop, DataPropertyClass):
                        instance_roles.append({'role': prop.name, 'value': value})
            instances.append({'instance_name': instance_name, 'properties': instance_roles})
        onto.destroy()
        return InstancesModelOut(model_id=model_id, class_name=class_name, instances=instances)

    def delete_instance(self, model_id: int, class_name: str, instance_label: str):
        """
                        Delete instance with a given label
        """
        onto = self.model_service.load_ontology(model_id)
        if onto is None:
            return InstanceModelOut(errors="Model with id " + str(model_id) + " not found")
        owl_class = onto[class_name]
        if owl_class is None:
            onto.destroy()
            return InstanceModelOut(errors="Class named " + str(class_name) + " not found in Model " + str(model_id))

        instance = onto.search_one(is_a=owl_class,label=instance_label)
        if instance is None:
            onto.destroy()
            return InstanceModelOut(
                errors="Instance with label " + str(instance_label) + " not found in Model " + str(model_id))
        else:
            instance_id = instance.name
            destroy_entity(instance)
            self.model_service.update_ontology(model_id, onto)
            return FullInstanceModelOut(instance_id=instance_id, label=instance_label)


