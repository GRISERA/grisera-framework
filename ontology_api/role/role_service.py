from owlready2 import get_ontology
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
        onto.destroy()
        return ObjectPropertyRoleModelOut()
        