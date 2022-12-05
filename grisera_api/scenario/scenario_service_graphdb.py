from graph_api_service import GraphApiService
from scenario.scenario_model import ScenarioIn, ScenarioOut, OrderChangeIn, OrderChangeOut
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from activity_execution.activity_execution_model import ActivityExecutionOut, PropertyIn, ActivityExecutionIn
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from scenario.scenario_service import ScenarioService


class ScenarioServiceGraphDB(ScenarioService):
    """
    Object to handle logic of scenarios requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_execution_service (ActivityExecutionService): Service used to communicate with ActivityExecution
    experiment_service (ExperimentService): Service used to communicate with Experiment
    """
    graph_api_service = GraphApiService()
    activity_execution_service = ActivityExecutionServiceGraphDB()
    experiment_service = ExperimentServiceGraphDB()

    def save_scenario(self, scenario: ScenarioIn):
        """
        Send request to graph api to create new scenario

        Args:
            scenario (ScenarioIn): Scenario to be added

        Returns:
            Result of request as scenario object
        """
        activity_executions = [
            self.activity_execution_service.save_activity_execution(activity_execution=activity_execution) for
            activity_execution in scenario.activity_executions]
        self.graph_api_service.create_relationships(scenario.experiment_id, activity_executions[0].id,
                                                    'hasScenario')
        [self.graph_api_service.create_relationships(activity_executions[index - 1].id, activity_executions[index].id,
                                                     'nextActivityExecution')
         for index in range(1, len(activity_executions))]

        return ScenarioOut(experiment_id=scenario.experiment_id, activity_executions=activity_executions)

    def add_activity_execution(self, previous_id: int, activity_execution: ActivityExecutionIn):
        """
        Send request to graph api to add activity_execution to scenario

        Args:
            previous_id (int): Id of previous activity_execution or experiment
            activity_execution (ActivityExecutionIn): ActivityExecution to be added

        Returns:
            Result of request as activity_execution object
        """
        relationships = self.graph_api_service.get_node_relationships(previous_id)['relationships']
        activity_execution_result = self.activity_execution_service.save_activity_execution(activity_execution)

        if previous_id in [relation['start_node'] for relation in relationships if
                           relation['name'] == 'hasScenario']:
            self.graph_api_service.create_relationships(previous_id, activity_execution_result.id,
                                                        'hasScenario')
        else:
            self.graph_api_service.create_relationships(previous_id, activity_execution_result.id,
                                                        'nextActivityExecution')

        try:
            next_id, relation_id = [(relation['end_node'], relation['id']) for relation in relationships
                                    if relation['name'] in ['hasScenario', 'nextActivityExecution']
                                    and relation['start_node'] == previous_id][0]
        except IndexError:
            return activity_execution_result

        self.graph_api_service.create_relationships(activity_execution_result.id, next_id, 'nextActivityExecution')
        self.graph_api_service.delete_relationship(relation_id)

        return activity_execution_result

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
        start_node, end_node, relation_name = (
            middle_relationships[0]['start_node'], last_id,
            middle_relationships[0]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        if middle_relationships[1] == last_relationships[0]:
            # nodes are next to each other
            start_node, end_node, relation_name = (
                last_id, middle_relationships[1]['start_node'],
                middle_relationships[1]['name']
            )
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)

            return

        # nodes are separated by other nodes
        start_node, end_node, relation_name = (
            last_id, middle_relationships[1]['end_node'],
            middle_relationships[1]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        start_node, end_node, relation_name = (
            last_relationships[0]['start_node'], middle_id,
            last_relationships[0]['name']
        )
        if start_node != end_node:
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        return

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
        start_node, end_node, relation_name = (
            middle_relationships[0]['start_node'], last_id,
            middle_relationships[0]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        if middle_relationships[1] == last_relationships[0]:
            # nodes are next to each other
            start_node, end_node, relation_name = (
                last_id, middle_id,
                middle_relationships[1]['name']
            )
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)

            start_node, end_node, relation_name = (
                middle_id, last_relationships[1]['end_node'],
                last_relationships[1]['name']
            )
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)

            return

        start_node, end_node, relation_name = (
            last_id, middle_relationships[1]['end_node'],
            middle_relationships[1]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        start_node, end_node, relation_name = (
            last_relationships[0]['start_node'], middle_id,
            last_relationships[0]['name']
        )
        if start_node != end_node:
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        start_node, end_node, relation_name = (
            middle_id, last_relationships[1]['end_node'],
            last_relationships[1]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)

        return

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
        p_relationships = previous_relationships
        p_count = False
        a_relationships = activity_execution_relationships
        a_count = False
        while True:
            if p_relationships[0]['name'] is not None and p_relationships[0]['name'] in ['hasScenario']:
                p_count = True
                break
            if a_relationships[0]['name'] is not None and a_relationships[0]['name'] in ['hasScenario']:
                a_count = True
                break
            p_id = p_relationships[0]['start_node']
            p_relationships = self.graph_api_service.get_node_relationships(p_id)['relationships']
            p_relationships = [relation for relation in p_relationships
                               if relation['name'] in ['nextActivityExecution', 'hasScenario']
                               and relation['end_node'] == p_id]
            a_id = a_relationships[0]['start_node']
            a_relationships = self.graph_api_service.get_node_relationships(a_id)['relationships']
            a_relationships = [relation for relation in a_relationships
                               if relation['name'] in ['nextActivityExecution', 'hasScenario']
                               and relation['end_node'] == a_id]

        return p_count, a_count

    def swap_order_in_relationships_array(self, relationships, node_id):
        """
            Swaps order of relationships list so they are saved in order starting from experiment
            Args:
                relationships: List of relationships
                node_id: Id of node, that relationships belong to
            Returns:
                relationships: List of relationships in specified order
        """
        if relationships[0]['start_node'] == node_id:
            relationships[0], relationships[1] = relationships[1], relationships[0]

        return relationships

    def change_order(self, order_change: OrderChangeIn):
        """
        Send request to graph api to change order in scenario

        Args:
            order_change (OrderChangeIn): Ids of activity_executions to change order by

        Returns:
            Result of request as changed order ids
        """
        # save all relationships in lists
        previous_relationships = self.graph_api_service.get_node_relationships(order_change.previous_id)[
            'relationships']
        activity_execution_relationships = \
            self.graph_api_service.get_node_relationships(order_change.activity_execution_id)['relationships']

        # check which node is before the other
        previous_first, activity_execution_first = self.what_order(previous_relationships,
                                                                   activity_execution_relationships)

        # delete nextActivityExecution and hasScenario relationships 
        [self.graph_api_service.delete_relationship(relation['id']) for relation in previous_relationships
         if relation['name'] in ['nextActivityExecution', 'hasScenario']]
        [self.graph_api_service.delete_relationship(relation['id']) for relation in activity_execution_relationships
         if relation['name'] in ['nextActivityExecution', 'hasScenario']]

        # save nextActivityExecution and hasScenario relationships 
        previous_relationships = [relation for relation in previous_relationships
                                  if relation['name'] in ['nextActivityExecution', 'hasScenario']]
        activity_execution_relationships = [relation for relation in activity_execution_relationships
                                            if relation['name'] in ['nextActivityExecution', 'hasScenario']]

        # swap order of relationships if needed
        previous_relationships = self.swap_order_in_relationships_array(previous_relationships,
                                                                        order_change.previous_id)
        activity_execution_relationships = self.swap_order_in_relationships_array(activity_execution_relationships,
                                                                                  order_change.activity_execution_id)

        if len(activity_execution_relationships) == 1:
            # change order when activity execution node is last
            self.change_order_middle_with_last(middle_id=order_change.previous_id,
                                               last_id=order_change.activity_execution_id,
                                               middle_relationships=previous_relationships,
                                               last_relationships=activity_execution_relationships)

        elif len(previous_relationships) == 1:
            # change order when previous node is last
            self.change_order_middle_with_last(middle_id=order_change.activity_execution_id,
                                               last_id=order_change.previous_id,
                                               middle_relationships=activity_execution_relationships,
                                               last_relationships=previous_relationships)

        elif len(previous_relationships) == 2 and len(activity_execution_relationships) == 2:
            if previous_first is True:
                # change order when previous node is before activity execution node
                self.change_order_middle_with_middle(middle_id=order_change.previous_id,
                                                     last_id=order_change.activity_execution_id,
                                                     middle_relationships=previous_relationships,
                                                     last_relationships=activity_execution_relationships)
            elif activity_execution_first is True:
                # change order when activity execution node is before previous node
                self.change_order_middle_with_middle(middle_id=order_change.activity_execution_id,
                                                     last_id=order_change.previous_id,
                                                     middle_relationships=activity_execution_relationships,
                                                     last_relationships=previous_relationships)

        return OrderChangeOut(previous_id=order_change.previous_id,
                              activity_execution_id=order_change.activity_execution_id)

    def delete_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to delete activity_execution from scenario

        Args:
            activity_execution_id (int): Id of activity_execution to delete

        Returns:
            Result of request as activity_execution object
        """
        relationships = self.graph_api_service.get_node_relationships(activity_execution_id)['relationships']
        if len(relationships) == 0:
            return ActivityExecutionOut(errors='Relationships not found')

        activity_execution = self.graph_api_service.delete_node(activity_execution_id)

        properties = {p['key']: p['value'] for p in activity_execution['properties']}
        additional_properties = [PropertyIn(key=key, value=value) for key, value in properties.items()
                                 if key not in ['activity']]
        activity_execution_response = ActivityExecutionOut(id=activity_execution['id'], activity=properties['activity'],
                                                           additional_properties=additional_properties)

        if len([relationship for relationship in relationships if
                relationship['name'] in ['hasScenario', 'nextActivityExecution']]) == 1:
            return activity_execution_response

        start_node = [relationship['start_node'] for relationship in relationships
                      if relationship['end_node'] == activity_execution_id and relationship['name']
                      in ['hasScenario', 'nextActivityExecution']][0]
        end_node = [relationship['end_node'] for relationship in relationships
                    if relationship['start_node'] == activity_execution_id
                    and relationship['name'] == 'nextActivityExecution'][0]
        self.graph_api_service.create_relationships(start_node, end_node, relationships[0]['name'])

        return activity_execution_response

    def get_scenario(self, node_id: int):
        """
        Send request to graph api to get activity executions and experiment from scenario

        Args:
            node_id (int): Id of experiment or activity execution which is included in scenario

        Returns:
            Result of request as Scenario object
        """
        get_response = self.graph_api_service.get_node(node_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=node_id, errors=get_response["errors"])
        if get_response["labels"][0] not in ["Activity Execution", "Experiment"]:
            return NotFoundByIdModel(id=node_id, errors="Node not found.")

        if get_response["labels"][0] == "Activity Execution":
            return self.get_scenario_by_activity_execution(node_id)
        elif get_response["labels"][0] == "Experiment":
            return self.get_scenario_by_experiment(node_id)

    def get_scenario_by_experiment(self, experiment_id: int):
        """
        Send request to graph api to get activity_executions from scenario which starts in experiment

        Args:
            experiment_id (int): Id of experiment where scenario starts

        Returns:
            Result of request as Scenario object
        """
        activity_executions = []

        experiment = self.experiment_service.get_experiment(experiment_id)
        if type(experiment) is NotFoundByIdModel:
            return experiment

        scenario = {'experiment_id': experiment_id, 'activity_executions': []}

        for relation in experiment.relations:
            if relation.name == "hasScenario":
                self.get_scenario_after_activity_execution(relation.second_node_id, activity_executions)

        [scenario['activity_executions'].append(a) for a in activity_executions if a not in scenario['activity_executions']]

        return ScenarioOut(**scenario)

    def get_scenario_by_activity_execution(self, activity_execution_id: int):
        """
        Send request to graph api to get activity_executions from scenario which has activity execution id incuded

        Args:
            activity_execution_id (int): Id of activity execution included in scenario

        Returns:
            Result of request as Scenario object
        """
        activity_executions = []
        activity_executions_before = []

        activity_execution = self.activity_execution_service.get_activity_execution(activity_execution_id)
        if type(activity_execution) is NotFoundByIdModel:
            return activity_execution

        experiment_id = self.get_scenario_before_activity_execution(activity_execution_id, activity_executions_before)
        [activity_executions.append(a) for a in activity_executions_before if a not in activity_executions]

        activity_executions_after = []

        self.get_scenario_after_activity_execution(activity_execution_id, activity_executions_after)
        [activity_executions.append(a) for a in activity_executions_after if a not in activity_executions]

        scenario = {'experiment_id': experiment_id,
                    'activity_executions': []}

        [scenario['activity_executions'].append(a) for a in activity_executions]

        return ScenarioOut(**scenario)

    def get_scenario_after_activity_execution(self, activity_execution_id: int, activity_executions: []):
        """
        Gets activity executions from scenario which are saved after activity_execution_id

        Args:
            activity_execution_id (int): Id of activity execution included in scenario
            activity_executions: List of activity executions in scenario
        """
        activity_execution = self.activity_execution_service.get_activity_execution(activity_execution_id)

        if type(activity_execution) is NotFoundByIdModel:
            return activity_execution

        activity_executions.append(activity_execution)

        for relation in activity_execution.relations:
            if relation.name == "nextActivityExecution":
                activity_execution = self.activity_execution_service.get_activity_execution(relation.second_node_id)

                if type(activity_execution) is NotFoundByIdModel:
                    return activity_execution

                activity_executions.append(activity_execution)
                [self.get_scenario_after_activity_execution(activity_execution.id, activity_executions)
                 for r in activity_execution.relations if r.name == "nextActivityExecution"]

    def get_scenario_before_activity_execution(self, activity_execution_id: int, activity_executions: []):
        """
        Gets activity executions from scenario which are saved before activity_execution_id

        Args:
            activity_execution_id (int): Id of activity execution included in scenario
            activity_executions: List of activity executions in scenario
        """
        activity_execution = self.activity_execution_service.get_activity_execution(activity_execution_id)
        if type(activity_execution) is NotFoundByIdModel:
            return activity_execution

        activity_executions.append(activity_execution)

        for relation in activity_execution.reversed_relations:

            if relation.name == "nextActivityExecution":
                activity_execution = self.activity_execution_service.get_activity_execution(relation.second_node_id)
                if type(activity_execution) is NotFoundByIdModel:
                    return activity_execution

                activity_executions.append(activity_execution)
                return self.get_scenario_before_activity_execution(activity_execution.id, activity_executions)

            elif relation.name == "hasScenario":
                experiment = self.experiment_service.get_experiment(relation.second_node_id)
                if type(experiment) is NotFoundByIdModel:
                    return experiment

                return experiment.id




