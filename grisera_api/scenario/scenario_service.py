from graph_api_service import GraphApiService
from scenario.scenario_model import ScenarioIn, ScenarioOut, OrderChangeIn, OrderChangeOut
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_model import ActivityExecutionOut, PropertyIn, ActivityExecutionIn
from experiment.experiment_service import ExperimentService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ScenarioService:
    """
    Object to handle logic of scenarios requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_execution_service (ActivityExecutionService): Service used to communicate with ActivityExecution
    experiment_service (ExperimentService): Service used to communicate with Experiment
    """
    graph_api_service = GraphApiService()
    activity_execution_service = ActivityExecutionService()
    experiment_service = ExperimentService()

    def save_scenario(self, scenario: ScenarioIn):
        """
        Send request to graph api to create new scenario

        Args:
            scenario (ScenarioIn): Scenario to be added

        Returns:
            Result of request as scenario object
        """
        print("save_scenario not implemented yet")

    def add_activity_execution(self, previous_id: int, activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to add activity_execution to scenario

        Args:
            previous_id (int): Id of previous activity_execution or experiment
            activity_execution (ActivityExecutionIn): ActivityExecution to be added

        Returns:
            Result of request as activity_execution object
        """
        print("add_activity_execution not implemented yet")

    def change_order_middle_with_last(self, middle_id, last_id, middle_relationships, last_relationships):
        """
            Changes order of the middle node and the last node

            Args:
                middle_id (int): Id of the middle node
                last_id (ActivityExecutionIn): Id of the last node
                middle_relationships: Relationships of the middle node
                last_relationships: Relationships of the last node
            Returns:
        """
        print("change_order_middle_with_last not implemented yet")

    def change_order_middle_with_middle(self, middle_id, last_id, middle_relationships, last_relationships):
        """
            Changes order of the two middle nodes

            Args:
                middle_id (int): Id of the middle node
                last_id (ActivityExecutionIn): Id of the middle node but second in order
                middle_relationships: Relationships of the middle node
                last_relationships: Relationships of the last node
            Returns:
        """
        print("change_order_middle_with_middle not implemented yet")

    def what_order(self, previous_relationships, activity_execution_relationships):
        """
            Finds which node is in which order (starting from experiment) in the scenario

            Args:
                previous_relationships: Relationships of the previous node
                activity_execution_relationships: Relationships of the activity execution node
            Returns:
                True when is the first in order
                False when is the second in order
        """
        print("what_order not implemented yet")

    def swap_order_in_relationships_array(self, relationships, node_id):
        """
            Swaps order of relationships list so they are saved in order starting from experiment
            Args:
                relationships: List of relationships
                node_id: Id of node, that relationships belong to
            Returns:
                relationships: List of relationships in specified order
        """
        print("swap_order_in_relationships_array not implemented yet")

    def change_order(self, order_change: OrderChangeIn):
        """
        Send request to graph api to change order in scenario

        Args:
            order_change (OrderChangeIn): Ids of activity_executions to change order by

        Returns:
            Result of request as changed order ids
        """
        print("change_order not implemented yet")

    def delete_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to delete activity_execution from scenario

        Args:
            activity_execution_id (int): Id of activity_execution to delete

        Returns:
            Result of request as activity_execution object
        """
        print("delete_activity_execution not implemented yet")

    def get_scenario(self, node_id: int):
        """
        Send request to graph api to get activity executions and experiment from scenario

        Args:
            node_id (int): Id of experiment or activity execution which is included in scenario

        Returns:
            Result of request as Scenario object
        """
        print("get_scenario not implemented yet")

    def get_scenario_by_experiment(self, experiment_id: int):
        """
        Send request to graph api to get activity_executions from scenario which starts in experiment

        Args:
            experiment_id (int): Id of experiment where scenario starts

        Returns:
            Result of request as Scenario object
        """
        print("get_scenario_by_experiment not implemented yet")

    def get_scenario_by_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to get activity_executions from scenario which has activity execution id incuded

        Args:
            activity_execution_id (int): Id of activity execution included in scenario

        Returns:
            Result of request as Scenario object
        """
        print("get_scenario_by_activity_execution not implemented yet")

    def get_scenario_after_activity_execution(self, activity_execution_id: int, activity_executions: []):
        """
        Gets activity executions from scenario which are saved after activity_execution_id

        Args:
            activity_execution_id (int): Id of activity execution included in scenario
            activity_executions: List of activity executions in scenario
        """
        print("get_scenario_after_activity_execution not implemented yet")

    def get_scenario_before_activity_execution(self, activity_execution_id: int, activity_executions: []):
        """
        Gets activity executions from scenario which are saved before activity_execution_id

        Args:
            activity_execution_id (int): Id of activity execution included in scenario
            activity_executions: List of activity executions in scenario
        """
        print("get_scenario_before_activity_execution not implemented yet")




