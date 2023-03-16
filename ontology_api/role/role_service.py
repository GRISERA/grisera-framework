from datetime import datetime
from owlready2 import FunctionalProperty, ObjectPropertyClass
from role.role_model import RoleModelIn, RoleModelOut
from model.model_service import ModelService


class RoleService:
    """
        Object to handle logic of role requests
    """

    def __init__(self):
        self.model_service = ModelService()

    def add_role(self, model_id: int, model_in: RoleModelIn):
        """
                Create an instance of an object property in the given model
        """
        onto = self.model_service.load_ontology(model_id)

        if onto is None:
            return RoleModelOut(errors=f"Model with id {model_id} not found")

        onto_property = onto[model_in.role]

        if onto_property is None:
            onto.destroy()
            return RoleModelOut(errors=f"Property {model_in.role} not found")

        property_domain = onto_property.domain
        property_range = onto_property.range
        instance = onto.search_one(type=property_domain, iri=f"*{model_in.instance_name}")

        if instance is None:
            onto.destroy()
            return RoleModelOut(errors=f"Instance {model_in.instance_name} not found")

        if isinstance(onto_property, ObjectPropertyClass):

            value = onto.search_one(type=property_range, iri=f"*{model_in.value}")
            if value is None:
                onto.destroy()
                return RoleModelOut(errors=f"Instance {model_in.value} not found")

        else:

            if property_range[0] == int:
                if isinstance(model_in.value, str):
                    try:
                        value = int(model_in.value)
                    except ValueError:
                        onto.destroy()
                        return RoleModelOut(errors=f"Wrong type of value")
                else:
                    value = model_in.value

            elif isinstance(model_in.value, str) and property_range[0] == datetime:
                #   use for datetime type ISO 8601, example: "2023-03-12T14:55:00Z"
                try:
                    value = datetime.strptime(model_in.value, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    onto.destroy()
                    return RoleModelOut(
                        errors=f"Wrong format of date. Example: '2023-03-12T14:55:00Z'.")

            elif not isinstance(model_in.value, property_range[0]):
                onto.destroy()
                return RoleModelOut(errors=f"Wrong type of value")

            else:
                value = model_in.value

        if FunctionalProperty in onto_property.is_a:
            setattr(instance, model_in.role, value)
        else:
            if getattr(instance, model_in.role) is not None:
                getattr(instance, model_in.role).append(value)
            else:
                setattr(instance, model_in.role, [value])

        model_out = self.model_service.update_ontology(model_id, onto)

        if model_out.errors is not None:
            return RoleModelOut(errors=model_out.errors)

        return RoleModelOut(role=model_in.role, instance_name=model_in.instance_name,
                            value=model_in.value)
