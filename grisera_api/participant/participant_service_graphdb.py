from graph_api_service import GraphApiService
from participant.participant_model import ParticipantIn, ParticipantsOut, BasicParticipantOut, ParticipantOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation
from participant.participant_service import ParticipantService


class ParticipantServiceGraphDB(ParticipantService):
    """
    Object to handle logic of participants requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_participant(self, participant: ParticipantIn, database_name: str):
        """
        Send request to graph api to create new participant

        Args:
            participant (ParticipantIn): Participant to be added

        Returns:
            Result of request as participant object
        """
        node_response = self.graph_api_service.create_node("Participant", database_name)

        if node_response["errors"] is not None:
            return ParticipantOut(**participant.dict(), errors=node_response["errors"])

        participant_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(participant_id, participant, database_name)
        if properties_response["errors"] is not None:
            return ParticipantOut(**participant.dict(), errors=properties_response["errors"])

        return ParticipantOut(**participant.dict(), id=participant_id)

    def get_participants(self, database_name: str):
        """
        Send request to graph api to get participants

        Returns:
            Result of request as list of participants objects
        """
        get_response = self.graph_api_service.get_nodes("Participant", database_name)

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

    def get_participant(self, participant_id: int, database_name: str):
        """
        Send request to graph api to get given participant

        Args:
            participant_id (int): Id of participant

        Returns:
            Result of request as participant object
        """
        get_response = self.graph_api_service.get_node(participant_id, database_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participant_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Participant":
            return NotFoundByIdModel(id=participant_id, errors="Node not found.")

        participant = {'id': get_response['id'], 'additional_properties': [], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] in ["name", "date_of_birth", "sex", "disorder"]:
                participant[property["key"]] = property["value"]
            else:
                participant['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(participant_id, database_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == participant_id:
                participant['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                    name=relation["name"], relation_id=relation["id"]))
            else:
                participant['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                             name=relation["name"],
                                                                             relation_id=relation["id"]))

        return ParticipantOut(**participant)

    def delete_participant(self, participant_id: int, database_name: str):
        """
        Send request to graph api to delete given participant

        Args:
            participant_id (int): Id of participant

        Returns:
            Result of request as participant object
        """
        get_response = self.get_participant(participant_id, database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(participant_id, database_name)
        return get_response

    def update_participant(self, participant_id: int, participant: ParticipantIn, database_name: str):
        """
        Send request to graph api to update given participant

        Args:
            participant_id (int): Id of participant
            participant (ParticipantIn): Properties to update

        Returns:
            Result of request as participant object
        """
        get_response = self.get_participant(participant_id, database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if participant.date_of_birth is not None:
            participant.date_of_birth = participant.date_of_birth.__str__()

        self.graph_api_service.delete_node_properties(participant_id, database_name)
        self.graph_api_service.create_properties(participant_id, participant, database_name)

        participant_result = {"id": participant_id, 'relations': get_response.relations,
                              'reversed_relations': get_response.reversed_relations}
        participant_result.update(participant.dict())

        return ParticipantOut(**participant_result)
