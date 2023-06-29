import unittest
import unittest.mock as mock

from activity.activity_model import ActivityOut, ActivityIn
from activity.activity_service_ontology import ActivityServiceOntology
from ontology_api_service import OntologyApiService
from property.property_model import PropertyIn


class TestActivityServicePut(unittest.TestCase):

    @mock.patch.object(OntologyApiService, 'add_role')
    @mock.patch.object(OntologyApiService, 'delete_roles')
    @mock.patch.object(ActivityServiceOntology, 'get_activity')
    def test_update_activity_without_error(self, get_activity_mock, delete_roles_mock, add_role_mock):
        model_id = 1
        activity_name = "test"
        delete_roles_mock.return_value = {'errors': None}
        add_role_mock.return_value = {'errors': None}
        get_activity_mock.return_value = ActivityOut(activity="individual", activity_name=activity_name,
                                                     additional_properties=[], activity_executions=[], errors=None)

        additional_properties = [PropertyIn(key='test', value='test')]
        activity = ActivityIn(activity="individual", activity_name=activity_name,
                              additional_properties=additional_properties)
        activity_service = ActivityServiceOntology()

        result = activity_service.update_activity(model_id, activity)

        self.assertEqual(result, ActivityOut(activity="individual", activity_executions=[], activity_name=activity_name,
                                             additional_properties=additional_properties))

        add_role_mock.assert_called_once_with(model_id, 'test', 'test', 'test')
        delete_roles_mock.assert_called_once_with(model_id, 'test')
        get_activity_mock.assert_called_once_with(activity_name)

    @mock.patch.object(ActivityServiceOntology, 'get_activity')
    def test_update_experiment_with_error(self, get_activity_mock):
        model_id = 1
        activity_name = "test"
        get_activity_mock.return_value = ActivityOut(activity="individual", activity_name=activity_name,
                                                     additional_properties=[], activity_executions=[], errors="error")

        additional_properties = [PropertyIn(key='test', value='test')]
        activity = ActivityIn(activity="individual", activity_name=activity_name,
                              additional_properties=additional_properties)
        activity_service = ActivityServiceOntology()

        result = activity_service.update_activity(model_id, activity)

        self.assertEqual(result, ActivityOut(activity="individual", activity_name=activity_name, errors="error",
                                             additional_properties=additional_properties))

        get_activity_mock.assert_called_once_with(activity_name)
