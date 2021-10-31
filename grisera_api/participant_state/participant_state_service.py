from graph_api_service import GraphApiService
from participant.participant_service import ParticipantService
from personality.personality_service import PersonalityService
from appearance.appearance_service import AppearanceService
from participant_state.participant_state_model import ParticipantStatePropertyIn, BasicParticipantStateOut, \
    ParticipantStatesOut, ParticipantStateOut, ParticipantStateIn, ParticipantStateRelationIn
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ParticipantStateService:
    """
    Object to handle logic of participant state requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        participant_service (ParticipantService): Service to manage participant models
    """
    graph_api_service = GraphApiService()
    participant_service = ParticipantService()
    appearance_service = AppearanceService()
    personality_service = PersonalityService()

    def save_participant_state(self, participant_state: ParticipantStateIn):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """
        node_response = self.graph_api_service.create_node("`Participant State`")

        if node_response["errors"] is not None:
            return ParticipantStateOut(**participant_state.dict(), errors=node_response["errors"])

        participant_state_id = node_response["id"]

        if participant_state.participant_id is not None and \
                type(self.participant_service.get_participant(participant_state.participant_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.participant_id,
                                                        name="hasParticipant")
        if participant_state.personality_id is not None and \
                type(self.personality_service.get_personality(participant_state.personality_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.personality_id,
                                                        name="hasPersonality")
        if participant_state.appearance_id is not None and \
                type(self.appearance_service.get_appearance(participant_state.appearance_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.appearance_id,
                                                        name="hasAppearance")

        participant_state.participant_id = participant_state.personality_id = participant_state.appearance_id = None
        self.graph_api_service.create_properties(participant_state_id, participant_state)

        return self.get_participant_state(participant_state_id)

    def get_participant_states(self):
        """
        Send request to graph api to get participant states

        Returns:
            Result of request as list of participant states objects
        """
        get_response = self.graph_api_service.get_nodes("`Participant State`")

        participant_states = []

        for participant_state_node in get_response["nodes"]:
            properties = {'id': participant_state_node['id'], 'additional_properties': []}
            for property in participant_state_node["properties"]:
                if property["key"] == "age":
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            participant_state = BasicParticipantStateOut(**properties)
            participant_states.append(participant_state)

        return ParticipantStatesOut(participant_states=participant_states)

    def get_participant_state(self, participant_state_id: int):
        """
        Send request to graph api to get given participant state

        Args:
            participant_state_id (int): Id of participant state

        Returns:
            Result of request as participant state object
        """
        get_response = self.graph_api_service.get_node(participant_state_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participant_state_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Participant State":
            return NotFoundByIdModel(id=participant_state_id, errors="Node not found.")

        participant_state = {'id': get_response['id'], 'additional_properties': [], 'relations': [],
                             'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] == "age":
                participant_state[property["key"]] = property["value"]
            else:
                participant_state['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(participant_state_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == participant_state_id:
                participant_state['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                          name=relation["name"],
                                                                          relation_id=relation["id"]))
            else:
                participant_state['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                                   name=relation["name"],
                                                                                   relation_id=relation["id"]))

        return ParticipantStateOut(**participant_state)

    def delete_participant_state(self, participant_state_id: int):
        """
        Send request to graph api to delete given participant state

        Args:
            participant_state_id (int): Id of participant state

        Returns:
            Result of request as participant state object
        """
        get_response = self.get_participant_state(participant_state_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(participant_state_id)
        return get_response

    def update_participant_state(self, participant_state_id: int, participant_state: ParticipantStatePropertyIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int): Id of participant state
            participant_state (ParticipantStatePropertyIn): Properties to update

        Returns:
            Result of request as participant state object
        """
        get_response = self.get_participant_state(participant_state_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.create_properties(participant_state_id, participant_state)

        participant_state_result = {"id": participant_state_id, "relations": get_response.relations,
                                    "reversed_relations": get_response.reversed_relations}
        participant_state_result.update(participant_state.dict())

        return ParticipantStateOut(**participant_state_result)

    def update_participant_state_relationships(self, participant_state_id: int,
                                               participant_state: ParticipantStateRelationIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int): Id of participant state
            participant_state (ParticipantStateRelationIn): Relationships to update

        Returns:
            Result of request as participant state object
        """
        get_response = self.get_participant_state(participant_state_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if participant_state.participant_id is not None and \
                type(self.participant_service.get_participant(
                    participant_state.participant_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.participant_id,
                                                        name="hasParticipant")
        if participant_state.personality_id is not None and \
                type(self.personality_service.get_personality(participant_state.personality_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.personality_id,
                                                        name="hasPersonality")
        if participant_state.appearance_id is not None and \
                type(self.appearance_service.get_appearance(participant_state.appearance_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.appearance_id,
                                                        name="hasAppearance")

        return self.get_participant_state(participant_state_id)
