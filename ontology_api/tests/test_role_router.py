import asyncio
import unittest
import os
from datetime import datetime
from owlready2 import get_ontology
from role.role_model import ObjectPropertyRoleModelIn, ObjectPropertyRoleModelOut, DataTypePropertyRoleModelIn
from role.role_router import RoleRouter
from fastapi import Response


class RoleRouterTestCase(unittest.TestCase):
    def test_add_object_property_role_without_error(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        src = onto["ParticipantState"]("ps")
        dst = onto["Participant"]("p")
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = ObjectPropertyRoleModelIn(src_instance_name="ps", dst_instance_name="p", role_name="hasParticipant")
        result = asyncio.run(role_router.add_object_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 200)
        onto = get_ontology("database" + os.path.sep + f"{model_id}.owl").load()
        self.assertEqual(onto["ps"].hasParticipant, onto["p"])
        onto.destroy()
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_object_property_role_model_does_not_exist(self):
        role_router = RoleRouter()
        response = Response()
        model_in = ObjectPropertyRoleModelIn(src_instance_name="ps", dst_instance_name="p", role_name="hasParticipant")
        model_id = 1
        result = asyncio.run(role_router.add_object_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.errors, f"Model with id {model_id} not found")

    def test_add_object_property_role_instance_not_found(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = ObjectPropertyRoleModelIn(src_instance_name="ps", dst_instance_name="p", role_name="hasParticipant")
        result = asyncio.run(role_router.add_object_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.errors, f"Instance ps not found")
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_object_property_role_property_does_not_exist(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        src = onto["ParticipantState"]("ps")
        dst = onto["Participant"]("p")
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = ObjectPropertyRoleModelIn(src_instance_name="ps", dst_instance_name="p", role_name="notHere")
        result = asyncio.run(role_router.add_object_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.errors, f"Property {model_in.role_name} not found")
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_datatype_property_role_wrong_type_of_value(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        src = onto["ParticipantState"]("ps")
        value = "123"
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = DataTypePropertyRoleModelIn(src_instance_name="ps", value=value, role_name="age")
        result = asyncio.run(role_router.add_datatype_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.errors, f"Wrong type of value")
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_datatype_property_role_without_error(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        src = onto["ParticipantState"]("ps")
        value = 123
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = DataTypePropertyRoleModelIn(src_instance_name="ps", value=value, role_name="age")
        result = asyncio.run(role_router.add_datatype_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 200)
        onto = get_ontology("database" + os.path.sep + f"{model_id}.owl").load()
        self.assertEqual(onto["ps"].age, value)
        onto.destroy()
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_datatype_property_role_wrong_format_of_date(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        src = onto["Participant"]("ps")
        value = "2001.01.01"
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = DataTypePropertyRoleModelIn(src_instance_name="ps", value=value, role_name="dateOfBirth")
        result = asyncio.run(role_router.add_datatype_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.errors, f"Wrong format of date. Example: '2023-03-12T14:55:00Z'.")
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_datatype_property_role_correct_format_of_date(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        src = onto["Participant"]("ps")
        value = "2023-03-12T14:55:00Z"
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = DataTypePropertyRoleModelIn(src_instance_name="ps", value=value, role_name="dateOfBirth")
        result = asyncio.run(role_router.add_datatype_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 200)
        onto = get_ontology("database" + os.path.sep + f"{model_id}.owl").load()
        self.assertEqual(onto["ps"].dateOfBirth, datetime(2023, 3, 12, 14, 55, 00))
        onto.destroy()
        os.remove("database" + os.path.sep + f"{model_id}.owl")

    def test_add_datatype_property_role_instance_not_found(self):
        role_router = RoleRouter()
        response = Response()
        model_id = 1
        onto = get_ontology("https://road.affectivese.org/documentation/owlAC.owl").load()
        onto.save(file="database" + os.path.sep + f"{model_id}.owl", format="rdfxml")
        onto.destroy()
        model_in = DataTypePropertyRoleModelIn(src_instance_name="ps", value=0, role_name="hasParticipant")
        result = asyncio.run(role_router.add_datatype_property_role(model_id, model_in, response))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.errors, f"Instance ps not found")
        os.remove("database" + os.path.sep + f"{model_id}.owl")