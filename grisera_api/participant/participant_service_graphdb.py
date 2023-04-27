from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from participant.participant_model import ParticipantIn, ParticipantsOut, BasicParticipantOut, ParticipantOut
from models.not_found_model import NotFoundByIdModel
from participant.participant_service import ParticipantService


class ParticipantServiceGraphDB(ParticipantService):
    """
    Object to handle logic of participants requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.participant_state_service = None

    def save_participant(self, participant: ParticipantIn):
        """
        Send request to graph api to create new participant

        Args:
            participant (ParticipantIn): Participant to be added

        Returns:
            Result of request as participant object
        """
        node_response = self.graph_api_service.create_node("Participant")

        if node_response["errors"] is not None:
            return ParticipantOut(**participant.dict(), errors=node_response["errors"])

        participant_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(participant_id, participant)
        if properties_response["errors"] is not None:
            return ParticipantOut(**participant.dict(), errors=properties_response["errors"])

        return ParticipantOut(**participant.dict(), id=participant_id)

    def get_participants(self):
        """
        Send request to graph api to get participants

        Returns:
            Result of request as list of participants objects
        """
        get_response = self.graph_api_service.get_nodes("Participant")

        participants = []

        for participant_node in get_response["nodes"]:
            properties = {'id': participant_node['id'], 'additional_properties': []}
            for property in participant_node["properties"]:
                if property["key"] in ["name", "date_of_birth", "sex", "disorder"]:
                    properties[property["key"]] = property["value"]
                else:
                    properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            participant = BasicParticipantOut(**properties)
            participants.append(participant)

        return ParticipantsOut(participants=participants)

    def get_participant(self, participant_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given participant

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participant_id (int | str): identity of participant

        Returns:
            Result of request as participant object
        """
        get_response = self.graph_api_service.get_node(participant_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participant_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Participant":
            return NotFoundByIdModel(id=participant_id, errors="Node not found.")

        participant = create_stub_from_response(get_response, properties=['name', 'date_of_birth', 'sex', 'disorder'])

        if depth != 0:
            participant["participant_states"] = []
            relations_response = self.graph_api_service.get_node_relationships(participant_id)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == participant_id & relation["name"] == "hasParticipantState":
                    participant['participant_states'].append(self.participant_state_service.
                                                             get_participant_state(relation["end_node"],
                                                                                   depth - 1))

            return ParticipantOut(**participant)
        else:
            return BasicParticipantOut(**participant)

    def delete_participant(self, participant_id: Union[int, str]):
        """
        Send request to graph api to delete given participant

        Args:
            participant_id (int): Id of participant

        Returns:
            Result of request as participant object
        """
        get_response = self.get_participant(participant_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(participant_id)
        return get_response

    def update_participant(self, participant_id: Union[int, str], participant: ParticipantIn):
        """
        Send request to graph api to update given participant

        Args:
            participant_id (int | str): Id of participant
            participant (ParticipantIn): Properties to update

        Returns:
            Result of request as participant object
        """
        get_response = self.get_participant(participant_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if participant.date_of_birth is not None:
            participant.date_of_birth = participant.date_of_birth.__str__()

        self.graph_api_service.delete_node_properties(participant_id)
        self.graph_api_service.create_properties(participant_id, participant)

        participant_result = {"id": participant_id}
        participant_result.update(participant.dict())

        return BasicParticipantOut(**participant_result)
