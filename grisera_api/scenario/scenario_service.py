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
                                                    'hasActivityExecution')
        [self.graph_api_service.create_relationships(activity_executions[index - 1].id, activity_executions[index].id,
                                                     'next')
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
                           relation['name'] == 'hasActivityExecution']:
            self.graph_api_service.create_relationships(previous_id, activity_execution_result.id,
                                                        'hasActivityExecution')
        else:
            self.graph_api_service.create_relationships(previous_id, activity_execution_result.id, 'next')

        try:
            next_id, relation_id = [(relation['end_node'], relation['id']) for relation in relationships
                                    if relation['name'] in ['hasActivityExecution', 'next']
                                    and relation['start_node'] == previous_id][0]
        except IndexError:
            return activity_execution_result

        self.graph_api_service.create_relationships(activity_execution_result.id, next_id, 'next')
        self.graph_api_service.delete_relationship(relation_id)

        return activity_execution_result

    def change_order(self, order_change: OrderChangeIn):
        """
        Send request to graph api to change order in scenario

        Args:
            order_change (OrderChangeIn): Ids of activity_executions to change order by

        Returns:
            Result of request as changed order ids
        """
        relationships = self.graph_api_service.get_node_relationships(order_change.previous_id)['relationships']
        activity_execution_relationships = \
        self.graph_api_service.get_node_relationships(order_change.activity_execution_id)['relationships']

        [self.graph_api_service.delete_relationship(relation['id']) for relation in activity_execution_relationships
         if relation['name'] in ['next', 'hasActivityExecution']]

        if len(activity_execution_relationships) == 2:
            start_node, end_node = (
            activity_execution_relationships[0]['start_node'], activity_execution_relationships[1]['end_node']) \
                if activity_execution_relationships[0]['end_node'] == order_change.activity_execution_id \
                else (
            activity_execution_relationships[1]['start_node'], activity_execution_relationships[0]['end_node'])
            self.graph_api_service.create_relationships(start_node, end_node, 'next')

        if order_change.previous_id in [relation['start_node'] for relation in relationships
                                        if relation['name'] == 'hasActivityExecution']:
            self.graph_api_service.create_relationships(order_change.previous_id, order_change.activity_execution_id,
                                                        'hasActivityExecution')
        else:
            self.graph_api_service.create_relationships(order_change.previous_id, order_change.activity_execution_id,
                                                        'next')

        try:
            next_id, relation_id = [(relation['end_node'], relation['id']) for relation in relationships
                                    if relation['name'] in ['hasActivityExecution', 'next']
                                    and relation['start_node'] == order_change.previous_id][0]
        except IndexError:
            return OrderChangeOut(previous_id=order_change.previous_id,
                                  activity_execution_id=order_change.activity_execution_id)

        self.graph_api_service.create_relationships(order_change.activity_execution_id, next_id, 'next')
        self.graph_api_service.delete_relationship(relation_id)

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
            return ActivityExecutionOut(identifier=0, errors='Relationships not found')

        activity_execution = self.graph_api_service.delete_node(activity_execution_id)

        properties = {property['key']: property['value'] for property in activity_execution['properties']}
        additional_properties = [PropertyIn(key=key, value=value) for key, value in properties.items()
                                 if key not in ['identifier', 'name', 'activity', 'layout']]
        activity_execution_response = ActivityExecutionOut(id=activity_execution['id'],
                                                           identifier=properties['identifier'], name=properties['name'],
                                                           activity=properties['activity'], layout=properties['layout'],
                                                           additional_properties=additional_properties)

        if len([relationship for relationship in relationships if relationship['name'] in ['hasActivity', 'next']]) == 1:
            return activity_response
        if len(relationships) == 1:
            return activity_execution_response

        start_node = [relationship['start_node'] for relationship in relationships
                      if relationship['end_node'] == activity_id and relationship['name'] in ['hasActivity', 'next']][0]
        end_node = [relationship['end_node'] for relationship in relationships
                    if relationship['start_node'] == activity_id and relationship['name'] == 'next'][0]
        start_node, end_node = (relationships[0]['start_node'], relationships[1]['end_node']) \
            if relationships[0]['end_node'] == activity_execution_id \
            else (relationships[1]['start_node'], relationships[0]['end_node'])
        self.graph_api_service.create_relationships(start_node, end_node, relationships[0]['name'])

        return activity_execution_response
