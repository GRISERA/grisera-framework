from graph_api_service import GraphApiService
from scenario.scenario_model import ScenarioIn, ScenarioOut, OrderChangeIn, OrderChangeOut
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_model import ActivityExecutionOut, PropertyIn, ActivityExecutionIn


class ScenarioService:
    """
    Object to handle logic of scenarios requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        activity_execution_service (ActivityExecutionService): Service used to communicate with ActivityExecution
    """
    graph_api_service = GraphApiService()
    activity_execution_service = ActivityExecutionService()

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
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

        if middle_relationships[1] == last_relationships[0]:
            # nodes are next to each other
            start_node, end_node, relation_name = (
                last_id, middle_relationships[1]['start_node'],
                middle_relationships[1]['name']
            )
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)
            print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

            return

        # nodes are separated by other nodes
        start_node, end_node, relation_name = (
            last_id, middle_relationships[1]['end_node'],
            middle_relationships[1]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

        start_node, end_node, relation_name = (
            last_relationships[0]['start_node'], middle_id,
            last_relationships[0]['name']
        )
        if start_node != end_node:
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

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
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

        if middle_relationships[1] == last_relationships[0]:
            # nodes are next to each other
            start_node, end_node, relation_name = (
                last_id, middle_id,
                middle_relationships[1]['name']
            )
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)
            print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

            start_node, end_node, relation_name = (
                middle_id, last_relationships[1]['end_node'],
                last_relationships[1]['name']
            )
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)
            print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

            return

        start_node, end_node, relation_name = (
            last_id, middle_relationships[1]['end_node'],
            middle_relationships[1]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

        start_node, end_node, relation_name = (
            last_relationships[0]['start_node'], middle_id,
            last_relationships[0]['name']
        )
        if start_node != end_node:
            self.graph_api_service.create_relationships(start_node, end_node, relation_name)
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

        start_node, end_node, relation_name = (
            middle_id, last_relationships[1]['end_node'],
            last_relationships[1]['name']
        )
        self.graph_api_service.create_relationships(start_node, end_node, relation_name)
        print("start_node = ", start_node, "end_node = ", end_node, "name = ", relation_name)

        return

    def what_order(self, previous_relationships, activity_execution_relationships):
        """
            Finds which node is in which order in the scenario
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

    def change_order(self, order_change: OrderChangeIn):
        """
        Send request to graph api to change order in scenario

        Args:
            order_change (OrderChangeIn): Ids of activity_executions to change order by

        Returns:
            Result of request as changed order ids
        """
        previous_relationships = self.graph_api_service.get_node_relationships(order_change.previous_id)[
            'relationships']
        activity_execution_relationships = \
            self.graph_api_service.get_node_relationships(order_change.activity_execution_id)['relationships']

        previous_first, activity_execution_first = self.what_order(previous_relationships,
                                                                   activity_execution_relationships)

        [self.graph_api_service.delete_relationship(relation['id']) for relation in previous_relationships
         if relation['name'] in ['nextActivityExecution', 'hasScenario']]
        [self.graph_api_service.delete_relationship(relation['id']) for relation in activity_execution_relationships
         if relation['name'] in ['nextActivityExecution', 'hasScenario']]

        previous_relationships = [relation for relation in previous_relationships
                                  if relation['name'] in ['nextActivityExecution', 'hasScenario']]
        activity_execution_relationships = [relation for relation in activity_execution_relationships
                                            if relation['name'] in ['nextActivityExecution', 'hasScenario']]

        if len(activity_execution_relationships) == 1:
            print('a last')
            self.change_order_middle_with_last(middle_id=order_change.previous_id,
                                               last_id=order_change.activity_execution_id,
                                               middle_relationships=previous_relationships,
                                               last_relationships=activity_execution_relationships)

        elif len(previous_relationships) == 1:
            print('p last')
            self.change_order_middle_with_last(middle_id=order_change.activity_execution_id,
                                               last_id=order_change.previous_id,
                                               middle_relationships=activity_execution_relationships,
                                               last_relationships=previous_relationships)

        elif len(previous_relationships) == 2 and len(activity_execution_relationships) == 2:
            if previous_first is True:
                print('p before a')
                self.change_order_middle_with_middle(middle_id=order_change.previous_id,
                                                     last_id=order_change.activity_execution_id,
                                                     middle_relationships=previous_relationships,
                                                     last_relationships=activity_execution_relationships)
            elif activity_execution_first is True:
                print('a before p')
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
