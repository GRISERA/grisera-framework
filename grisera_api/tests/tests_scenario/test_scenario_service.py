import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from scenario.scenario_model import *
from scenario.scenario_service import ScenarioService, ActivityService


class TestScenarioService(unittest.TestCase):

    @mock.patch.object(ActivityService, 'save_activity')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_scenario_without_error(self, create_relationships_mock, save_activity_mock):
        id_node = 1
        activity_out = ActivityOut(identifier=1, id=2)
        save_activity_mock.return_value = activity_out
        create_relationships_mock.return_value = activity_out
        calls = [mock.call(2, 2, 'hasActivity')]
        scenario = ScenarioIn(experiment_id=2, activities=[ActivityIn(identifier=1)])
        scenario_service = ScenarioService()

        result = scenario_service.save_scenario(scenario)

        self.assertEqual(result, ScenarioOut(experiment_id=2, activities=[activity_out], id=id_node))
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(ActivityService, 'save_activity')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_after_experiment(self, delete_relationship_mock, create_relationships_mock,
                                           get_node_relationships_mock, save_activity_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 1, 'end_node': 2,
                                                                       'name': 'hasActivity', 'id': 0}]}
        activity = ActivityIn(identifier=0, name='Test')
        save_activity_mock.return_value = ActivityOut(identifier=0, name='Test', id=3)
        calls = [mock.call(1, 3, 'hasActivity'), mock.call(3, 2, 'next')]
        scenario_service = ScenarioService()

        result = scenario_service.add_activity(1, activity)

        self.assertEqual(result, ActivityOut(identifier=0, name='Test', id=3))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_called_once_with(0)
        save_activity_mock.assert_called_with(activity)

    @mock.patch.object(ActivityService, 'save_activity')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_at_end(self, delete_relationship_mock, create_relationships_mock,
                                 get_node_relationships_mock, save_activity_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 0, 'end_node': 1,
                                                                       'name': 'next', 'id': 0}
                                                                      ]}
        activity = ActivityIn(identifier=0, name='Test')
        save_activity_mock.return_value = ActivityOut(identifier=0, name='Test', id=3)
        calls = [mock.call(1, 3, 'next')]
        scenario_service = ScenarioService()

        result = scenario_service.add_activity(1, activity)

        self.assertEqual(result, ActivityOut(identifier=0, name='Test', id=3))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_not_called()
        save_activity_mock.assert_called_with(activity)

    @mock.patch.object(ActivityService, 'save_activity')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_in_middle(self, delete_relationship_mock, create_relationships_mock,
                                    get_node_relationships_mock, save_activity_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 1, 'end_node': 2,
                                                                       'name': 'next', 'id': 0},
                                                                      {'start_node': 2, 'end_node': 3,
                                                                       'name': 'next', 'id': 1}
                                                                      ]}
        activity = ActivityIn(identifier=0, name='Test')
        save_activity_mock.return_value = ActivityOut(identifier=0, name='Test', id=4)
        calls = [mock.call(2, 4, 'next'), mock.call(4, 3, 'next')]
        scenario_service = ScenarioService()

        result = scenario_service.add_activity(2, activity)

        self.assertEqual(result, ActivityOut(identifier=0, name='Test', id=4))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_called_once_with(1)
        save_activity_mock.assert_called_with(activity)


