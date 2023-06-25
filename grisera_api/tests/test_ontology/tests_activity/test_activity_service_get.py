import unittest
from unittest.mock import patch, MagicMock

from activity.activity_model import ActivityIn, ActivityOut, Activity
from activity.activity_service_ontology import ActivityServiceOntology
from ontology_api_service import OntologyApiService


class TestActivityServiceGetActivity(unittest.TestCase):

    @patch.object(OntologyApiService, 'get_instance')
    @patch.object(OntologyApiService, 'get_reversed_roles')
    def test_get_activity_individual(self, get_reversed_roles_mock, get_instance_mock):
        model_id = 1
        activity_id = "individual_activity"

        # Mock the responses
        get_instance_mock.return_value = {
            "activity_name": activity_id,
            "errors": None
        }
        get_reversed_roles_mock.return_value = {
            "roles": [
                {"role": "hasActivity", "value": activity_id, "instance_name": "execution_1"},
                {"role": "hasActivity", "value": activity_id, "instance_name": "execution_2"}
            ],
            "errors": None
        }

        activity_service = ActivityServiceOntology()

        result = activity_service.get_activity(activity_id)

        self.assertEqual(result, ActivityOut(
            activity_name=activity_id,
            additional_properties=[],
            activity=Activity.individual,
            activity_executions=[
                {"id": "execution_1"},
                {"id": "execution_2"}
            ],
            errors=None
        ))
        get_instance_mock.assert_called_once_with(model_id=model_id, class_name="IndividualActivity", instance_label=activity_id)
        get_reversed_roles_mock.assert_called_once_with(model_id, activity_id)

    @patch.object(OntologyApiService, 'get_instance')
    def test_get_activity_error(self, get_instance_mock):
        model_id = 1
        activity_id = "error_activity"
        get_instance_mock.return_value = {
            "activity_name": activity_id,
            "errors": "Error"
        }
        activity_service = ActivityServiceOntology()
        result = activity_service.get_activity(activity_id)
        self.assertEqual(result, ActivityOut(activity_name=activity_id,
                                             additional_properties=[],
                                             activity="two-people",
                                             activity_executions=None,
                                             errors="Error"))
