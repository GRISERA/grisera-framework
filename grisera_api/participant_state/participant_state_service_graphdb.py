from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from participant_state.participant_state_service import ParticipantStateService
from participant_state.participant_state_model import ParticipantStatePropertyIn, BasicParticipantStateOut, \
    ParticipantStatesOut, ParticipantStateOut, ParticipantStateIn, ParticipantStateRelationIn
from models.not_found_model import NotFoundByIdModel


class ParticipantStateServiceGraphDB(ParticipantStateService):
    """
    Object to handle logic of participant state requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        participant_service (ParticipantService): Service to manage participant models
        appearance_service (AppearanceService): Service to manage appearance models
        personality_service (PersonalityService): Service to manage personality models
    """
    graph_api_service = GraphApiService()

    def __init__(self, participant_service, appearance_service, personality_service, participation_service):
        self.participant_service = participant_service()
        self.appearance_service = appearance_service()
        self.personality_service = personality_service()
        self.participation_service = participation_service()

    def save_participant_state(self, participant_state: ParticipantStateIn):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """
        node_response = self.graph_api_service.create_node("Participant State")

        if node_response["errors"] is not None:
            return ParticipantStateOut(**participant_state.dict(), errors=node_response["errors"])

        participant_state_id = node_response["id"]

        if participant_state.participant_id is not None and \
                type(self.participant_service.get_participant(participant_state.participant_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.participant_id,
                                                        name="hasParticipant")
        for personality_id in participant_state.personality_ids:
            if personality_id is not None and \
                    type(self.personality_service.get_personality(personality_id)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=personality_id,
                                                            name="hasPersonality")
        for appearance_id in participant_state.appearance_ids:
            if appearance_id is not None and \
                    type(self.appearance_service.get_appearance(appearance_id)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=appearance_id,
                                                            name="hasAppearance")

        participant_state.participant_id = None
        participant_state.personality_ids = participant_state.appearance_ids = None
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

    def get_participant_state(self, participant_state_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given participant state

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participant_state_id (int | str): identity of participant state

        Returns:
            Result of request as participant state object
        """
        get_response = self.graph_api_service.get_node(participant_state_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participant_state_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Participant State":
            return NotFoundByIdModel(id=participant_state_id, errors="Node not found.")

        participant_state = create_stub_from_response(get_response)

        if depth != 0:
            participant_state["participant"] = None
            participant_state['participations'] = []
            participant_state['appearances'] = []
            participant_state["personalities"] = []
            relations_response = self.graph_api_service.get_node_relationships(participant_state_id)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == participant_state_id & relation["name"] == "hasParticipant":
                    participant_state["participant"] = self.participant_service.get_participant(relation["end_node"],
                                                                                                depth - 1)
                else:
                    if relation["end_node"] == participant_state_id & relation["name"] == "hasParticipantState":
                        participant_state['participations']. \
                            append(self.participation_service.get_participation(relation["start_node"], depth - 1))
                    else:
                        if relation["start_node"] == participant_state_id & relation["name"] == "hasAppearance":
                            participant_state['appearances'].append(
                                self.appearance_service.get_appearance(relation["end_node"], depth - 1))
                        else:
                            if relation["start_node"] == participant_state_id & relation["name"] == "hasPersonality":
                                participant_state['personalities'].append(self.personality_service.get_personality(
                                    relation["end_node"], depth - 1))

            return ParticipantStateOut(**participant_state)
        else:
            return BasicParticipantStateOut(**participant_state)

    def delete_participant_state(self, participant_state_id: Union[int, str]):
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

    def update_participant_state(self, participant_state_id: Union[int, str],
                                 participant_state: ParticipantStatePropertyIn):
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

        self.graph_api_service.delete_node_properties(participant_state_id)
        self.graph_api_service.create_properties(participant_state_id, participant_state)

        participant_state_result = {"id": participant_state_id, "participant": get_response.participant,
                                    "personalities": get_response.personalities,
                                    "appearances": get_response.appearances,
                                    "participations": get_response.participations}
        participant_state_result.update(participant_state.dict())

        return ParticipantStateOut(**participant_state_result)

    def update_participant_state_relationships(self, participant_state_id: Union[int, str],
                                               participant_state: ParticipantStateRelationIn):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int | str): identity of participant state
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
        for personality_id in participant_state.personality_ids:
            if personality_id is not None and \
                    type(self.personality_service.get_personality(
                        personality_id)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=personality_id,
                                                            name="hasPersonality")
        for appearance_id in participant_state.appearance_ids:
            if appearance_id is not None and \
                    type(self.appearance_service.get_appearance(appearance_id)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=appearance_id,
                                                            name="hasAppearance")

        return self.get_participant_state(participant_state_id)
