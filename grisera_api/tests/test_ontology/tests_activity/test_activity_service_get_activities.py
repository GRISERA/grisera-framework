import unittest
from unittest import mock

from activity.activity_model import ActivitiesOut, ActivityOut
from activity.activity_service_ontology import ActivityServiceOntology

from ontology_api_service import OntologyApiService


class TestActivityServiceGetActivities(unittest.TestCase):
    @mock.patch.object(ActivityServiceOntology, 'get_activity')
    @mock.patch.object(OntologyApiService, 'get_instances')
    def test_get_activities_without_error(self, get_instances_mock, get_activity_mock):
        model_id = 1
        activities = [ActivityOut(instance_name="BBB", activity_executions=[], activity="individual"),
                      ActivityOut(instance_name="AAA", activity_executions=[], activity="group")]

        #  get_instances_mock.return_value = {'errors': None, 'instances': activity_instances}
        get_instances_mock.side_effect = [
            {"instances": [{'instance_name': "BBB", 'properties': []}], "errors": None},
            {"instances": [], "errors": None},
            {"instances": [{'instance_name': "AAA", 'properties': []}], "errors": None}
        ]

        get_activity_mock.side_effect = [
            ActivityOut(instance_name="BBB", activity_executions=[], activity="individual"),
            ActivityOut(instance_name="AAA", activity_executions=[], activity="group")
        ]

        activity_service = ActivityServiceOntology()
        result = activity_service.get_activities()

        self.assertEqual(result, ActivitiesOut(activities=activities))

        get_instances_mock.assert_has_calls([
            mock.call(model_id, 'IndividualActivity'),
            mock.call(model_id, 'TwoPersonsActivity'),
            mock.call(model_id, 'GroupActivity')
        ])
        get_activity_mock.assert_has_calls([
            mock.call('BBB'),
            mock.call('AAA')
        ])

    @mock.patch.object(OntologyApiService, 'get_instances')
    def test_get_activities_with_error(self, get_instances_mock):
        model_id = 1

        get_instances_mock.side_effect = [
            {"instances": [{'instance_name': "BBB", 'properties': []}], "errors": 'ERROR'},
            {"instances": [], "errors": None},
            {"instances": [{'instance_name': "AAA", 'properties': []}], "errors": None}
        ]

        activity_service = ActivityServiceOntology()
        result = activity_service.get_activities()

        self.assertEqual(result, ActivitiesOut(activities=[], errors=['ERROR']))

        get_instances_mock.assert_has_calls([
            mock.call(model_id, 'IndividualActivity'),
            mock.call(model_id, 'TwoPersonsActivity'),
            mock.call(model_id, 'GroupActivity')
        ])
