from graph_api_service import GraphApiService
from personality.personality_model import PersonalityBigFiveIn, PersonalityBigFiveOut, \
    PersonalityPanasIn, PersonalityPanasOut, BasicPersonalityBigFiveOut, BasicPersonalityPanasOut, PersonalitiesOut
from models.relation_information_model import RelationInformation
from models.not_found_model import NotFoundByIdModel


class PersonalityService:
    """
    Abstract class to handle logic of personality requests

    """

    def save_personality_big_five(self, personality: PersonalityBigFiveIn):
        """
        Send request to graph api to create new personality big five model

        Args:
            personality (PersonalityBigFiveIn): Personality big five to be added

        Returns:
            Result of request as personality big five object
        """
        raise Exception("save_personality_big_five not implemented yet")

    def save_personality_panas(self, personality: PersonalityPanasIn):
        """
        Send request to graph api to create new personality panas model

        Args:
            personality (PersonalityPanasIn): Personality to be added

        Returns:
            Result of request as personality panas object
        """
        raise Exception("save_personality_panas not implemented yet")

    def get_personality(self, personality_id: int):
        """
        Send request to graph api to get given personality

        Args:
            personality_id (int): Id of personality

        Returns:
            Result of request as personality object
        """
        raise Exception("get_personality not implemented yet")

    def get_personalities(self):
        """
        Send request to graph api to get personalities

        Returns:
            Result of request as list of personalities objects
        """
        raise Exception("get_personalities not implemented yet")

    def delete_personality(self, personality_id: int):
        """
        Send request to graph api to delete given personality

        Args:
            personality_id (int): Id of personality

        Returns:
            Result of request as personality object
        """
        raise Exception("delete_personality not implemented yet")

    def update_personality_big_five(self, personality_id: int, personality: PersonalityBigFiveIn):
        """
        Send request to graph api to update given personality big five model

        Args:
            personality_id (int): Id of personality
            personality (PersonalityBigFiveIn): Properties to update

        Returns:
            Result of request as personality object
        """
        raise Exception("update_personality_big_five not implemented yet")

    def update_personality_panas(self, personality_id: int, personality: PersonalityPanasIn):
        """
        Send request to graph api to update given personality panas model

        Args:
            personality_id (int): Id of personality
            personality (PersonalityPanasIn): Properties to update

        Returns:
            Result of request as personality object
        """
        raise Exception("update_personality_panas not implemented yet")
