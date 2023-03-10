from owlready2 import get_ontology, FunctionalProperty
from role.role_model import ObjectPropertyRoleModelIn
from role.role_model import ObjectPropertyRoleModelOut
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
        code = f"""
        if FunctionalProperty in onto_property.is_a:
            src_instance.{model_in.role_name} = dst_instance
        else:
            if src_instance.{model_in.role_name} is not None:
                src_instance.{model_in.role_name}.append(dst_instance)
            else:
                src_instance.{model_in.role_name} = [dst_instance]                
        """
        exec(code)

        model_out = self.model_service.update_ontology(model_id, onto)

        if model_out.errors is not None:
            return ObjectPropertyRoleModelOut(errors=model_out.errors)

        return ObjectPropertyRoleModelOut(role_name=model_in.role_name, src_instance_name=model_in.src_instance_name,
                                          dst_instance_name=model_in.dst_instance_name)
        