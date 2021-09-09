from graph_api_service import GraphApiService
from personality.personality_model import PersonalityBigFiveIn, PersonalityBigFiveOut, \
    PersonalityPanasIn, PersonalityPanasOut


class PersonalityService:
    """
    Object to handle logic of personality requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_personality_big_five(self, personality: PersonalityBigFiveIn):
        """
        Send request to graph api to create new personality big five model

        Args:
            personality (PersonalityBigFiveIn): Personality big five to be added

        Returns:
            Result of request as personality big five object
        """

        if not 0 <= personality.agreeableness <= 1 or not 0 <= personality.conscientiousness <= 1 or \
           not 0 <= personality.extroversion <= 1 or not 0 <= personality.neuroticism <= 1 or \
           not 0 <= personality.openess <= 1:
            return PersonalityBigFiveOut(agreeableness=personality.agreeableness,
                                         conscientiousness=personality.conscientiousness,
                                         extroversion=personality.extroversion, neuroticism=personality.neuroticism,
                                         openess=personality.openess, errors="Value not between 0 and 1")

        node_response = self.graph_api_service.create_node("Personality")
        if node_response["errors"] is not None:
            return PersonalityBigFiveOut(agreeableness=personality.agreeableness,
                                         conscientiousness=personality.conscientiousness,
                                         extroversion=personality.extroversion, neuroticism=personality.neuroticism,
                                         openess=personality.openess, errors=node_response["errors"])

        personality_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(personality_id, personality)
        if properties_response["errors"] is not None:
            return PersonalityBigFiveOut(agreeableness=personality.agreeableness,
                                         conscientiousness=personality.conscientiousness,
                                         extroversion=personality.extroversion, neuroticism=personality.neuroticism,
                                         openess=personality.openess, errors=properties_response["errors"])

        return PersonalityBigFiveOut(agreeableness=personality.agreeableness,
                                     conscientiousness=personality.conscientiousness,
                                     extroversion=personality.extroversion, neuroticism=personality.neuroticism,
                                     openess=personality.openess, id=personality_id)

    def save_personality_panas(self, personality: PersonalityPanasIn):
        """
        Send request to graph api to create new personality panas model

        Args:
            personality (PersonalityPanasIn): Personality to be added

        Returns:
            Result of request as personality panas object
        """
        if not 0 <= personality.negative_affect <= 1 or not 0 <= personality.positive_affect <= 1:
            return PersonalityPanasOut(negative_affect=personality.negative_affect,
                                       positive_affect=personality.positive_affect, errors="Value not between 0 and 1")

        node_response = self.graph_api_service.create_node("Personality")
        if node_response["errors"] is not None:
            return PersonalityPanasOut(negative_affect=personality.negative_affect,
                                       positive_affect=personality.positive_affect, errors=node_response["errors"])

        personality_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(personality_id, personality)
        if properties_response["errors"] is not None:
            return PersonalityPanasOut(negative_affect=personality.negative_affect,
                                       positive_affect=personality.positive_affect, errors=properties_response["errors"])

        return PersonalityPanasOut(negative_affect=personality.negative_affect,
                                   positive_affect=personality.positive_affect, id=personality_id)
