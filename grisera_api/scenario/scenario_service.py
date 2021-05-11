from graph_api_service import GraphApiService
from scenario.scenario_model import ScenarioIn, ScenarioOut
from activity.activity_service import ActivityService


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
        activities = []
        previous_activity = None
        for activity in scenario.activities:
            # Create Nodes Activity for scenario
            actual_activity = self.activity_service.save_activity(activity=activity)
            if previous_activity is None:
                self.graph_api_service.create_relationships(scenario.experiment_id, actual_activity.id,
                                                            'hasActivity')
            else:
                self.graph_api_service.create_relationships(previous_activity.id, actual_activity.id, 'next')
            previous_activity = actual_activity
            activities.append(actual_activity)

        return ScenarioOut(experiment_id=scenario.experiment_id, activities=activities)
