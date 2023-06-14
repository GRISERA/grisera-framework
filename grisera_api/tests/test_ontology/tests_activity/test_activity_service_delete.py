import unittest
import unittest.mock as mock

from ontology_api_service import OntologyApiService
from activity.activity_model import *
from activity.activity_service_ontology import ActivityServiceOntology


class TestActivityServiceDelete(unittest.TestCase):

    @mock.patch.object(ActivityServiceOntology, 'get_activity')
    @mock.patch.object(OntologyApiService, 'delete_instance')
    def test_delete_activity_without_error(self, delete_instance_mock, get_activity_mock):
        activity_service = ActivityServiceOntology()
        model_id = 1
        activity_id = "JK"
        delete_instance_mock.return_value = {'instance_id': 'Test', 'label': activity_id, 'errors': None}
        get_activity_mock.return_value = {'activity': 'individual', 'additional_properties': [], 'activity_name':
            activity_id, 'errors': None}
        result = activity_service.delete_activity(model_id, activity_id)
        self.assertEqual(result, ActivityOut(id=activity_id, activity='individual'))
        delete_instance_mock.assert_called_once_with(model_id, "Activity", activity_id)

    @mock.patch.object(ActivityServiceOntology, 'get_activity')
    @mock.patch.object(OntologyApiService, 'delete_instance')
    def test_delete_activity_delete_error(self, delete_instance_mock, get_activity_mock):
        experiment_service = ActivityServiceOntology()
        model_id = 1
        activity_id = "JK"
        delete_instance_mock.return_value = {'instance_id': 'Test', 'label': activity_id, 'errors': 'error'}
        get_activity_mock.return_value = {'activity': 'individual', 'additional_properties': [], 'activity_name':
            activity_id, 'errors': None}
        result = experiment_service.delete_activity(model_id, activity_id)
        self.assertEqual(result, ActivityOut(id=activity_id, errors='error', activity='individual'))
        delete_instance_mock.assert_called_once_with(model_id, 'Activity', activity_id)

    @mock.patch.object(ActivityServiceOntology, 'get_activity')
    @mock.patch.object(OntologyApiService, 'delete_instance')
    def test_delete_activity_get_error(self, delete_instance_mock, get_activity_mock):
        experiment_service = ActivityServiceOntology()
        model_id = 1
        activity_id = "JK"
        delete_instance_mock.return_value = {'instance_id': 'Test', 'label': activity_id, 'errors': None}
        get_activity_mock.return_value = {'activity': 'individual', 'additional_properties': [], 'activity_name':
            activity_id, 'errors': 'error'}
        result = experiment_service.delete_activity(model_id, activity_id)
        self.assertEqual(result, ActivityOut(id=activity_id, errors='error', activity='individual'))
        delete_instance_mock.assert_not_called()
