import unittest
import unittest.mock as mock

from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from experiment.experiment_model import BasicExperimentOut
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from graph_api_service import GraphApiService
from scenario.scenario_model import *
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB


class TestScenarioService(unittest.TestCase):

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(ExperimentServiceGraphDB, 'get_experiment')
    def test_save_scenario_without_error(self, get_experiment_mock, create_relationships_mock,
                                         save_activity_execution_mock):
        id_node = 1
        activity_execution_out = ActivityExecutionOut(id=8)
        save_activity_execution_mock.return_value = activity_execution_out
        get_experiment_mock.return_value = BasicExperimentOut(id=2, experiment_name="TestExperiment")
        create_relationships_mock.return_value = activity_execution_out
        calls = [mock.call(2, 8, 'hasScenario')]
        scenario = ScenarioIn(experiment_id=2, activity_executions=[ActivityExecutionIn(activity_id=7,
                                                                                        arrangement_id=3)])
        scenario_service = ScenarioServiceGraphDB()
        scenario_service.activity_execution_service = mock.create_autospec(ActivityExecutionServiceGraphDB)
        scenario_service.activity_execution_service.save_activity_execution = save_activity_execution_mock

        scenario_service.experiment_service = mock.create_autospec(ExperimentServiceGraphDB)
        scenario_service.experiment_service.get_experiment = get_experiment_mock

        result = scenario_service.save_scenario(scenario)

        self.assertEqual(result, ScenarioOut(experiment=ExperimentOut(id=2, experiment_name="TestExperiment"),
                                             activity_executions=[ActivityExecutionOut(id=8)]))
        create_relationships_mock.assert_has_calls(calls)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_execution_after_experiment(self, delete_relationship_mock, create_relationships_mock,
                                                     get_node_relationships_mock, save_activity_execution_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 1, 'end_node': 2,
                                                                       'name': 'hasScenario', 'id': 0}]}
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3, identifier=0, name='Test')
        save_activity_execution_mock.return_value = ActivityExecutionOut(activity_id=1, arrangement_id=3,
                                                                         identifier=0, name='Test', id=3)
        calls = [mock.call(1, 3, 'hasScenario'), mock.call(3, 2, 'nextActivityExecution')]

        scenario_service = ScenarioServiceGraphDB()
        scenario_service.activity_execution_service = mock.create_autospec(ActivityExecutionServiceGraphDB)
        scenario_service.activity_execution_service.save_activity_execution = save_activity_execution_mock

        result = scenario_service.add_activity_execution(1, activity_execution)

        self.assertEqual(result, ActivityExecutionOut(activity_id=1, arrangement_id=3, identifier=0, name='Test', id=3))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_called_once_with(0)
        save_activity_execution_mock.assert_called_with(activity_execution)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'save_activity_execution')
    @mock.patch.object(GraphApiService, 'get_node_relationships')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'delete_relationship')
    def test_add_activity_execution_at_end(self, delete_relationship_mock, create_relationships_mock,
                                           get_node_relationships_mock, save_activity_execution_mock):
        get_node_relationships_mock.return_value = {'relationships': [{'start_node': 0, 'end_node': 1,
                                                                       'name': 'nextActivityExecution', 'id': 0}
                                                                      ]}
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3, identifier=0,
                                                 name='Test')
        save_activity_execution_mock.return_value = ActivityExecutionOut(id=3)
        calls = [mock.call(1, 3, 'nextActivityExecution')]

        scenario_service = ScenarioServiceGraphDB()
        scenario_service.activity_execution_service = mock.create_autospec(ActivityExecutionServiceGraphDB)
        scenario_service.activity_execution_service.save_activity_execution = save_activity_execution_mock

        result = scenario_service.add_activity_execution(1, activity_execution)

        self.assertEqual(result, ActivityExecutionOut(id=3))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_not_called()
        save_activity_execution_mock.assert_called_with(activity_execution)

    @mock.patch.object(ActivityExecutionServiceGraphDB, 'save_activity_execution')
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
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3, identifier=0, name='Test')
        save_activity_execution_mock.return_value = ActivityExecutionOut(id=4)
        calls = [mock.call(2, 4, 'nextActivityExecution'), mock.call(4, 3, 'nextActivityExecution')]
        scenario_service = ScenarioServiceGraphDB()
        scenario_service.activity_execution_service = mock.create_autospec(ActivityExecutionServiceGraphDB)
        scenario_service.activity_execution_service.save_activity_execution = save_activity_execution_mock

        result = scenario_service.add_activity_execution(2, activity_execution)

        self.assertEqual(result, ActivityExecutionOut(id=4))
        create_relationships_mock.assert_has_calls(calls)
        delete_relationship_mock.assert_called_once_with(1)
        save_activity_execution_mock.assert_called_with(activity_execution)
