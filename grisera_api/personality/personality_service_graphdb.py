from graph_api_service import GraphApiService
from personality.personality_model import PersonalityBigFiveIn, PersonalityBigFiveOut, \
    PersonalityPanasIn, PersonalityPanasOut, BasicPersonalityBigFiveOut, BasicPersonalityPanasOut, PersonalitiesOut
from models.relation_information_model import RelationInformation
from models.not_found_model import NotFoundByIdModel
from personality.personality_service import PersonalityService


class PersonalityServiceGraphDB(PersonalityService):
    """
    Object to handle logic of personality requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_personality_big_five(self, personality: PersonalityBigFiveIn, dataset_name: str):
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
            return PersonalityBigFiveOut(**personality.dict(), errors="Value not between 0 and 1")

        node_response = self.graph_api_service.create_node("Personality", dataset_name)
        personality_id = node_response["id"]
        self.graph_api_service.create_properties(personality_id, personality, dataset_name)
        return PersonalityBigFiveOut(**personality.dict(), id=personality_id)

    def save_personality_panas(self, personality: PersonalityPanasIn, dataset_name: str):
        """
        Send request to graph api to create new personality panas model

        Args:
            personality (PersonalityPanasIn): Personality to be added

        Returns:
            Result of request as personality panas object
        """
        if not 0 <= personality.negative_affect <= 1 or not 0 <= personality.positive_affect <= 1:
            return PersonalityPanasOut(**personality.dict(), errors="Value not between 0 and 1")

        node_response = self.graph_api_service.create_node("Personality", dataset_name)
        personality_id = node_response["id"]
        self.graph_api_service.create_properties(personality_id, personality, dataset_name)

        return PersonalityPanasOut(**personality.dict(), id=personality_id)

    def get_personality(self, personality_id: int, dataset_name: str):
        """
        Send request to graph api to get given personality

        Args:
            personality_id (int): Id of personality

        Returns:
            Result of request as personality object
        """
        get_response = self.graph_api_service.get_node(personality_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=personality_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Personality":
            return NotFoundByIdModel(id=personality_id, errors="Node not found.")

        personality = {'id': personality_id, 'relations': [], 'reversed_relations': []}
        personality.update({property["key"]: property["value"] for property in get_response["properties"]})

        relations_response = self.graph_api_service.get_node_relationships(personality_id, dataset_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == personality_id:
                personality["relations"].append(RelationInformation(second_node_id=relation["end_node"],
                                                                    name=relation["name"], relation_id=relation["id"]))
            else:
                personality["reversed_relations"].append(RelationInformation(second_node_id=relation["start_node"],
                                                                             name=relation["name"],
                                                                             relation_id=relation["id"]))

        return PersonalityPanasOut(**personality) if "negative_affect" in personality.keys() \
            else PersonalityBigFiveOut(**personality)

    def get_personalities(self, dataset_name: str):
        """
        Send request to graph api to get personalities

        Returns:
            Result of request as list of personalities objects
        """
        get_response = self.graph_api_service.get_nodes("Personality", dataset_name)

        personalities = []

        for personality_node in get_response["nodes"]:
            properties = {property["key"]: property["value"] for property in personality_node["properties"]}
            properties["id"] = personality_node["id"]
            personality = BasicPersonalityPanasOut(**properties) if "negative_affect" in properties.keys() \
                else BasicPersonalityBigFiveOut(**properties)
            personalities.append(personality)

        return PersonalitiesOut(personalities=personalities)

    def delete_personality(self, personality_id: int, dataset_name: str):
        """
        Send request to graph api to delete given personality

        Args:
            personality_id (int): Id of personality

        Returns:
            Result of request as personality object
        """
        get_response = self.get_personality(personality_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        self.graph_api_service.delete_node(personality_id, dataset_name)
        return get_response

    def update_personality_big_five(self, personality_id: int, personality: PersonalityBigFiveIn, dataset_name: str):
        """
        Send request to graph api to update given personality big five model

        Args:
            personality_id (int): Id of personality
            personality (PersonalityBigFiveIn): Properties to update

        Returns:
            Result of request as personality object
        """
        if not 0 <= personality.agreeableness <= 1 or not 0 <= personality.conscientiousness <= 1 or \
           not 0 <= personality.extroversion <= 1 or not 0 <= personality.neuroticism <= 1 or \
           not 0 <= personality.openess <= 1:
            return PersonalityBigFiveOut(**personality.dict(), errors="Value not between 0 and 1")

        get_response = self.get_personality(personality_id, dataset_name)
        if type(get_response) is NotFoundByIdModel:
            return get_response
        if type(get_response) is PersonalityPanasOut:
            return NotFoundByIdModel(id=personality_id, errors="Node not found.")

        self.graph_api_service.create_properties(personality_id, personality, dataset_name)
        personality_response = get_response.dict()
        personality_response.update(personality)
        return PersonalityBigFiveOut(**personality_response)

    def update_personality_panas(self, personality_id: int, personality: PersonalityPanasIn, dataset_name: str):
        """
        Send request to graph api to update given personality panas model

        Args:
            personality_id (int): Id of personality
            personality (PersonalityPanasIn): Properties to update

        Returns:
            Result of request as personality object
        """
        if not 0 <= personality.negative_affect <= 1 or not 0 <= personality.positive_affect <= 1:
            return PersonalityPanasOut(**personality.dict(), errors="Value not between 0 and 1")

        get_response = self.get_personality(personality_id, dataset_name)
        if type(get_response) is NotFoundByIdModel:
            return get_response
        if type(get_response) is PersonalityBigFiveOut:
            return NotFoundByIdModel(id=personality_id, errors="Node not found.")

        self.graph_api_service.create_properties(personality_id, personality, dataset_name)

        personality_response = get_response.dict()
        personality_response.update(personality)
        return PersonalityPanasOut(**personality_response)
