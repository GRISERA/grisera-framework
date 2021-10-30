import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from scenario.scenario_model import *
from scenario.scenario_service import ScenarioService, ActivityExecutionService


class TestScenarioService(unittest.TestCase):

    @mock.patch.object(ActivityExecutionService, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'create_relationships')
    def test_save_scenario_without_error(self, create_relationships_mock, save_activity_execution_mock):
        id_node = 1
        activity_execution_out = ActivityExecutionOut(activity='group',  id=2)
        save_activity_execution_mock.return_value = activity_execution_out
        create_relationships_mock.return_value = activity_execution_out
        calls = [mock.call(2, 2, 'hasScenario')]
        scenario = ScenarioIn(experiment_id=2, activity_executions=[ActivityExecutionIn(activity='group')])
        scenario_service = ScenarioService()

        result = scenario_service.save_scenario(scenario)

        self.assertEqual(result, ScenarioOut(experiment_id=2, activity_executions=[activity_execution_out], id=id_node))
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(ActivityExecutionService, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_execution_after_experiment(self, delete_relationship_mock, create_relationships_mock,
                                           get_node_relationships_mock, save_activity_execution_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 1, 'end_node': 2,
                                                                       'name': 'hasScenario', 'id': 0}]}
        activity_execution = ActivityExecutionIn(activity='group', identifier=0, name='Test')
        save_activity_execution_mock.return_value = ActivityExecutionOut(activity='group', identifier=0, name='Test', id=3)
        calls = [mock.call(1, 3, 'hasScenario'), mock.call(3, 2, 'nextActivityExecution')]
        scenario_service = ScenarioService()

        result = scenario_service.add_activity_execution(1, activity_execution)

        self.assertEqual(result, ActivityExecutionOut(activity='group', identifier=0, name='Test', id=3))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_called_once_with(0)
        save_activity_execution_mock.assert_called_with(activity_execution)

    @mock.patch.object(ActivityExecutionService, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_execution_at_end(self, delete_relationship_mock, create_relationships_mock,
                                 get_node_relationships_mock, save_activity_execution_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 0, 'end_node': 1,
                                                                       'name': 'nextActivityExecution', 'id': 0}
                                                                      ]}
        activity_execution = ActivityExecutionIn(activity='group', identifier=0, name='Test')
        save_activity_execution_mock.return_value = ActivityExecutionOut(activity='group', identifier=0, name='Test', id=3)
        calls = [mock.call(1, 3, 'nextActivityExecution')]
        scenario_service = ScenarioService()

        result = scenario_service.add_activity_execution(1, activity_execution)

        self.assertEqual(result, ActivityExecutionOut(activity='group', identifier=0, name='Test', id=3))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_not_called()
        save_activity_execution_mock.assert_called_with(activity_execution)

    @mock.patch.object(ActivityExecutionService, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_execution_in_middle(self, delete_relationship_mock, create_relationships_mock,
                                    get_node_relationships_mock, save_activity_execution_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 1, 'end_node': 2,
                                                                       'name': 'nextActivityExecution', 'id': 0},
                                                                      {'start_node': 2, 'end_node': 3,
                                                                       'name': 'nextActivityExecution', 'id': 1}
                                                                      ]}
        activity_execution = ActivityExecutionIn(activity='group', identifier=0, name='Test')
        save_activity_execution_mock.return_value = ActivityExecutionOut(activity='group', identifier=0, name='Test', id=4)
        calls = [mock.call(2, 4, 'nextActivityExecution'), mock.call(4, 3, 'nextActivityExecution')]
        scenario_service = ScenarioService()

        result = scenario_service.add_activity_execution(2, activity_execution)

        self.assertEqual(result, ActivityExecutionOut(activity='group', identifier=0, name='Test', id=4))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_called_once_with(1)
        save_activity_execution_mock.assert_called_with(activity_execution)

