from graph_api_service import GraphApiService
from scenario.scenario_model import ScenarioIn, ScenarioOut, OrderChangeIn, OrderChangeOut
from activity.activity_service import ActivityService
from activity.activity_model import ActivityOut, PropertyIn, ActivityIn


class ScenarioService:
    """
    Object to handle logic of scenarios requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        activity_service (ActivityService): Service used to communicate with Activity
    """
    graph_api_service = GraphApiService()
    activity_service = ActivityService()

    def save_scenario(self, scenario: ScenarioIn):
        """
        Send request to graph api to create new scenario

        Args:
            scenario (ScenarioIn): Scenario to be added

        Returns:
            Result of request as scenario object
        """
        activities = [self.activity_service.save_activity(activity=activity) for activity in scenario.activities]
        self.graph_api_service.create_relationships(scenario.experiment_id, activities[0].id, 'hasActivity')
        [self.graph_api_service.create_relationships(activities[index-1].id, activities[index].id, 'next')
         for index in range(1, len(activities))]

        return ScenarioOut(experiment_id=scenario.experiment_id, activities=activities)

    def add_activity(self, previous_id: int, activity: ActivityIn):
        """
        Send request to graph api to add activity to scenario

        Args:
            previous_id (int): Id of previous activity or experiment
            activity (ActivityIn): Activity to be added

        Returns:
            Result of request as activity object
        """
        relationships = self.graph_api_service.get_node_relationships(previous_id)['relationships']
        activity_result = self.activity_service.save_activity(activity)

        if previous_id in [relation['start_node'] for relation in relationships if relation['name'] == 'hasActivity']:
            self.graph_api_service.create_relationships(previous_id, activity_result.id, 'hasActivity')
        else:
            self.graph_api_service.create_relationships(previous_id, activity_result.id, 'next')

        try:
            next_id, relation_id = [(relation['end_node'], relation['id']) for relation in relationships
                                    if relation['name'] in ['hasActivity', 'next']
                                    and relation['start_node'] == previous_id][0]
        except IndexError:
            return activity_result

        self.graph_api_service.create_relationships(activity_result.id, next_id, 'next')
        self.graph_api_service.delete_relationship(relation_id)

        return activity_result

    def change_order(self, order_change: OrderChangeIn):
        """
        Send request to graph api to change order in scenario

        Args:
            order_change (OrderChangeIn): Ids of activities to change order by

        Returns:
            Result of request as changed order ids
        """
        relationships = self.graph_api_service.get_node_relationships(order_change.previous_id)['relationships']
        activity_relationships = self.graph_api_service.get_node_relationships(order_change.activity_id)['relationships']

        [self.graph_api_service.delete_relationship(relation['id']) for relation in activity_relationships
         if relation['name'] in ['next', 'hasActivity']]

        if len(activity_relationships) == 2:
            start_node, end_node = (activity_relationships[0]['start_node'], activity_relationships[1]['end_node']) \
                if activity_relationships[0]['end_node'] == order_change.activity_id \
                else (activity_relationships[1]['start_node'], activity_relationships[0]['end_node'])
            self.graph_api_service.create_relationships(start_node, end_node, 'next')

        if order_change.previous_id in [relation['start_node'] for relation in relationships
                                        if relation['name'] == 'hasActivity']:
            self.graph_api_service.create_relationships(order_change.previous_id, order_change.activity_id, 'hasActivity')
        else:
            self.graph_api_service.create_relationships(order_change.previous_id, order_change.activity_id, 'next')

        try:
            next_id, relation_id = [(relation['end_node'], relation['id']) for relation in relationships
                                    if relation['name'] in ['hasActivity', 'next']
                                    and relation['start_node'] == order_change.previous_id][0]
        except IndexError:
            return OrderChangeOut(previous_id=order_change.previous_id, activity_id=order_change.activity_id)

        self.graph_api_service.create_relationships(order_change.activity_id, next_id, 'next')
        self.graph_api_service.delete_relationship(relation_id)

        return OrderChangeOut(previous_id=order_change.previous_id, activity_id=order_change.activity_id)

    def delete_activity(self, activity_id: int):
        """
        Send request to graph api to delete activity from scenario

        Args:
            activity_id (int): Id of activity to delete

        Returns:
            Result of request as activity object
        """
        relationships = self.graph_api_service.get_node_relationships(activity_id)['relationships']
        if len(relationships) == 0:
            return ActivityOut(identifier=0, errors='Relationships not found')

        activity = self.graph_api_service.delete_node(activity_id)

        properties = {property['key']: property['value'] for property in activity['properties']}
        additional_properties = [PropertyIn(key=key, value=value) for key, value in properties.items()
                                 if key not in ['identifier', 'name', 'type', 'layout']]
        activity_response = ActivityOut(id=activity['id'], identifier=properties['identifier'], name=properties['name'],
                                        type=properties['type'], layout=properties['layout'],
                                        additional_properties=additional_properties)

        if len([relationship for relationship in relationships if relationship['name'] in ['hasActivity', 'next']]) == 1:
            return activity_response

        start_node = [relationship['start_node'] for relationship in relationships
                      if relationship['end_node'] == activity_id and relationship['name'] in ['hasActivity', 'next']][0]
        end_node = [relationship['end_node'] for relationship in relationships
                    if relationship['start_node'] == activity_id and relationship['name'] == 'next'][0]
        self.graph_api_service.create_relationships(start_node, end_node, relationships[0]['name'])

        return activity_response
