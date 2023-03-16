from datetime import datetime
from owlready2 import FunctionalProperty
from role.role_model import ObjectPropertyRoleModelIn, DataTypePropertyRoleModelIn
from role.role_model import ObjectPropertyRoleModelOut, DataTypePropertyRoleModelOut
from model.model_service import ModelService


class RoleService:
    """
        Object to handle logic of role requests
    """

    def __init__(self):
        self.model_service = ModelService()

    def add_object_property_role(self, model_id: int, model_in: ObjectPropertyRoleModelIn):
        """
                Create an instance of an object property in the given model
        """
        onto = self.model_service.load_ontology(model_id)

        if onto is None:
            return ObjectPropertyRoleModelOut(errors=f"Model with id {model_id} not found")

        onto_property = onto[model_in.role_name]

        if onto_property is None:
            onto.destroy()
            return ObjectPropertyRoleModelOut(errors=f"Property {model_in.role_name} not found")

        property_domain = onto_property.domain
        property_range = onto_property.range
        src_instance = onto.search_one(type=property_domain, iri=f"*{model_in.src_instance_name}")

        if src_instance is None:
            onto.destroy()
            return ObjectPropertyRoleModelOut(errors=f"Instance {model_in.src_instance_name} not found")

        dst_instance = onto.search_one(type=property_range, iri=f"*{model_in.dst_instance_name}")

        if dst_instance is None:
            onto.destroy()
            return ObjectPropertyRoleModelOut(errors=f"Instance {model_in.dst_instance_name} not found")

        if FunctionalProperty in onto_property.is_a:
            setattr(src_instance, model_in.role_name, dst_instance)
        else:
            if getattr(src_instance, model_in.role_name) is not None:
                getattr(src_instance, model_in.role_name).append(dst_instance)
            else:
                setattr(src_instance, model_in.role_name, [dst_instance])

        model_out = self.model_service.update_ontology(model_id, onto)

        if model_out.errors is not None:
            return ObjectPropertyRoleModelOut(errors=model_out.errors)

        return ObjectPropertyRoleModelOut(role_name=model_in.role_name, src_instance_name=model_in.src_instance_name,
                                          dst_instance_name=model_in.dst_instance_name)

    def add_datatype_property_role(self, model_id: int, model_in: DataTypePropertyRoleModelIn):
        """
                Create an instance of a datatype property in the given model
        """
        onto = self.model_service.load_ontology(model_id)

        if onto is None:
            return DataTypePropertyRoleModelOut(errors=f"Model with id {model_id} not found")

        onto_property = onto[model_in.role_name]

        if onto_property is None:
            onto.destroy()
            return DataTypePropertyRoleModelOut(errors=f"Property {model_in.role_name} not found")

        property_domain = onto_property.domain
        property_range = onto_property.range
        src_instance = onto.search_one(type=property_domain, iri=f"*{model_in.src_instance_name}")

        if src_instance is None:
            onto.destroy()
            return DataTypePropertyRoleModelOut(errors=f"Instance {model_in.src_instance_name} not found")

        if type(model_in.value) == str and property_range[0] == datetime:
            #   use for datetime type ISO 8601, example: "2023-03-12T14:55:00Z"
            try:
                value = datetime.strptime(model_in.value, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                onto.destroy()
                return DataTypePropertyRoleModelOut(errors=f"Wrong format of date. Example: '2023-03-12T14:55:00Z'.")
        elif type(model_in.value) != property_range[0]:
            onto.destroy()
            return DataTypePropertyRoleModelOut(errors=f"Wrong type of value")
        else:
            value = model_in.value

        if FunctionalProperty in onto_property.is_a:
            setattr(src_instance, model_in.role_name, value)
        else:
            if getattr(src_instance, model_in.role_name) is not None:
                getattr(src_instance, model_in.role_name).append(value)
            else:
                setattr(src_instance, model_in.role_name, [value])

        model_out = self.model_service.update_ontology(model_id, onto)

        if model_out.errors is not None:
            return DataTypePropertyRoleModelOut(errors=model_out.errors)

        return DataTypePropertyRoleModelOut(role_name=model_in.role_name, src_instance_name=model_in.src_instance_name,
                                            value=model_in.value)
