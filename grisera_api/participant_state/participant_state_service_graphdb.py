from typing import Union

from appearance.appearance_service import AppearanceService
from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from participant.participant_service import ParticipantService
from participant_state.participant_state_service import ParticipantStateService
from participant_state.participant_state_model import ParticipantStatePropertyIn, BasicParticipantStateOut, \
    ParticipantStatesOut, ParticipantStateOut, ParticipantStateIn, ParticipantStateRelationIn
from models.not_found_model import NotFoundByIdModel
from participation.participation_service import ParticipationService
from personality.personality_service import PersonalityService


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

    def __init__(self):
        self.participant_service: ParticipantService = None
        self.appearance_service: AppearanceService = None
        self.personality_service: PersonalityService = None
        self.participation_service: ParticipationService = None

    def save_participant_state(self, participant_state: ParticipantStateIn, dataset_name: str):
        """
        Send request to graph api to create new participant state

        Args:
            participant_state (ParticipantStateIn): Participant state to be added

        Returns:
            Result of request as participant state object
        """

        node_response = self.graph_api_service.create_node("`Participant State`", dataset_name)

        if node_response["errors"] is not None:
            return ParticipantStateOut(**participant_state.dict(), errors=node_response["errors"])

        participant_state_id = node_response["id"]

        if participant_state.participant_id is not None and \
                type(self.participant_service.get_participant(participant_state.participant_id,
                                                              dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.participant_id,
                                                        name="hasParticipant",
                                                        dataset_name=dataset_name)
        for personality_id in participant_state.personality_ids:
            if personality_id is not None and \
                    type(self.personality_service.get_personality(personality_id,
                                                                  dataset_name)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=personality_id,
                                                            name="hasPersonality",
                                                            dataset_name=dataset_name)
        for appearance_id in participant_state.appearance_ids:
            if appearance_id is not None and \
                    type(self.appearance_service.get_appearance(appearance_id, dataset_name)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=appearance_id,
                                                            name="hasAppearance",
                                                            dataset_name=dataset_name)

        participant_state.participant_id = None
        participant_state.personality_ids = participant_state.appearance_ids = None
        self.graph_api_service.create_properties(participant_state_id, participant_state, dataset_name)

        return self.get_participant_state(participant_state_id, dataset_name)

    def get_participant_states(self, dataset_name: str):
        """
        Send request to graph api to get participant states

        Returns:
            Result of request as list of participant states objects
        """
        get_response = self.graph_api_service.get_nodes("`Participant State`", dataset_name)

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

    def get_participant_state(self, participant_state_id: Union[int, str], dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given participant state

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participant_state_id (int | str): identity of participant state

        Returns:
            Result of request as participant state object
        """
        get_response = self.graph_api_service.get_node(participant_state_id, dataset_name)

        print("get_participant_state:  {}  {} {} ".format(participant_state_id, dataset_name, depth))

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participant_state_id, errors=get_response["errors"])

        print("get_response: {}".format(get_response))
        if get_response["labels"][0] != "Participant State":
            return NotFoundByIdModel(id=participant_state_id, errors="Node not found.")

        participant_state = create_stub_from_response(get_response, properties=['age'])

        if depth != 0:
            participant_state["participant"] = None
            participant_state['participations'] = []
            participant_state['appearances'] = []
            participant_state["personalities"] = []
            relations_response = self.graph_api_service.get_node_relationships(participant_state_id, dataset_name)

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
                                print("### here {} {} ".format(relation, participant_state_id))
                                participant_state['personalities'].append(self.personality_service.get_personality(
                                    relation["end_node"], depth - 1))

            return ParticipantStateOut(**participant_state)
        else:
            return BasicParticipantStateOut(**participant_state)

    def delete_participant_state(self, participant_state_id: Union[int, str], dataset_name: str):
        """
        Send request to graph api to delete given participant state

        Args:
            participant_state_id (int | str): Id of participant state

        Returns:
            Result of request as participant state object
        """
        get_response = self.get_participant_state(participant_state_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(participant_state_id, dataset_name)
        return get_response

    def update_participant_state(self, participant_state_id: Union[int, str],
                                 participant_state: ParticipantStatePropertyIn,
                                 dataset_name: str):

        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int): Id of participant state
            participant_state (ParticipantStatePropertyIn): Properties to update

        Returns:
            Result of request as participant state object
        """
        get_response = self.get_participant_state(participant_state_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(participant_state_id, dataset_name)
        self.graph_api_service.create_properties(participant_state_id, participant_state, dataset_name)

        participant_state_result = {"id": participant_state_id}
        participant_state_result.update(participant_state.dict())

        return BasicParticipantStateOut(**participant_state_result)

    def update_participant_state_relationships(self, participant_state_id: Union[int, str],
                                               participant_state: ParticipantStateRelationIn,
                                               dataset_name: str):
        """
        Send request to graph api to update given participant state

        Args:
            participant_state_id (int | str): identity of participant state
            participant_state (ParticipantStateRelationIn): Relationships to update

        Returns:
            Result of request as participant state object
        """
        get_response = self.get_participant_state(participant_state_id, dataset_name)

        print("get_response: {}".format(get_response))

        if type(get_response) is NotFoundByIdModel:
            return get_response

        # delete relationship between ParticipantState and Participant
        get_response_from_get = self.graph_api_service.get_node_relationships(participant_state_id, dataset_name)
        print("get_response_from_get ", get_response_from_get)
        for relationship in get_response_from_get['relationships']:
            if relationship['name'] == 'hasParticipant':
                participant_state_id_to_delete = relationship['id']
                print("participant_state_id_to_delete: ", participant_state_id_to_delete)

                get_response_delete = self.graph_api_service.delete_relationship(participant_state_id_to_delete, dataset_name)
                print("get_response_from_delete: ", get_response_delete)



        if participant_state.participant_id is not None and \
                type(self.participant_service.get_participant(
                    participant_state.participant_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                        end_node=participant_state.participant_id,
                                                        name="hasParticipant",
                                                        dataset_name=dataset_name)
        # for personality_id in participant_state.personality_ids:
        #     if personality_id is not None and \
        #             type(self.personality_service.get_personality(
        #                 personality_id, dataset_name)) is not NotFoundByIdModel:
        #         self.graph_api_service.create_relationships(start_node=participant_state_id,
        #                                                     end_node=personality_id,
        #                                                     name="hasPersonality",
        #                                                     dataset_name=dataset_name)
        for appearance_id in participant_state.appearance_ids:
            if appearance_id is not None and \
                    type(self.appearance_service.get_appearance(appearance_id, dataset_name)) is not NotFoundByIdModel:
                self.graph_api_service.create_relationships(start_node=participant_state_id,
                                                            end_node=appearance_id,
                                                            name="hasAppearance",
                                                            dataset_name=dataset_name)

        return self.get_participant_state(participant_state_id, dataset_name)
