import unittest
import unittest.mock as mock

from ontology_api_service import OntologyApiService
from activity.activity_model import *
from activity.activity_service_ontology import ActivityServiceOntology

class TestActivityServicePost(unittest.TestCase):

    @mock.patch.object(OntologyApiService, 'add_role')
    @mock.patch.object(OntologyApiService, 'add_instance')
    def test_save_activity_without_error(self, add_instance_mock, add_role_mock):
        activity_service = ActivityServiceOntology()
        model_id = 1
        activity_name = "JK"
        activity_type = Activity.individual
        add_instance_mock.return_value = {'label': activity_name, 'errors': None}
        add_role_mock.return_value = {'errors': None}
        additional_properties = [PropertyIn(key='test', value='tests')]
        activity = ActivityIn(activity=activity_type, activity_name=activity_name,
                              additional_properties=additional_properties)
        result = activity_service.save_activity(activity)

        self.assertEqual(result, ActivityOut(activity_name=activity_name, additional_properties=additional_properties,
                                             activity=activity_type))
        add_instance_mock.assert_called_once_with(model_id, 'IndividualActivity', activity_name)
        add_role_mock.assert_called_once_with(model_id, 'test', activity_name, 'tests')

    @mock.patch.object(OntologyApiService, 'add_instance')
    def test_save_activity_wrong_type(self, add_instance_mock):
        activity_service = ActivityServiceOntology()
        model_id = 1
        activity_name = "JK"
        activity_type = "lorem ipsum"
        additional_properties = [PropertyIn(key='test', value='test')]
        activity = ActivityIn(activity=activity_type, activity_name=activity_name,
                              additional_properties=additional_properties)
        result = activity_service.save_activity(activity)

        self.assertEqual(result.errors, f"Wrong type of activity: {activity_type}")
        

