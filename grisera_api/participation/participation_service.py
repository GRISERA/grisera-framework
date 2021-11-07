from graph_api_service import GraphApiService
from activity_execution.activity_execution_service import ActivityExecutionService
from participant_state.participant_state_service import ParticipantStateService
from participation.participation_model import ParticipationIn, ParticipationOut, ParticipationsOut, \
    BasicParticipationOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ParticipationService:
    """
    Object to handle logic of participation requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_execution_service (ActivityExecutionService): Service to send activity execution requests
    participant_state_service (ParticipantStateService): Service to send participant state requests
    """
    graph_api_service = GraphApiService()
    activity_execution_service = ActivityExecutionService()
    participant_state_service = ParticipantStateService()

    def save_participation(self, participation: ParticipationIn):
        """
        Send request to graph api to create new participation

        Args:
            participation (ParticipationIn): Participation to be added

        Returns:
            Result of request as participation object
        """
        node_response = self.graph_api_service.create_node("Participation")

        if node_response["errors"] is not None:
            return ParticipationOut(errors=node_response["errors"])

        participation_id = node_response["id"]

        if participation.activity_execution_id is not None and \
                type(self.activity_execution_service.get_activity_execution(participation.activity_execution_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(participation_id, participation.activity_execution_id,
                                                        "hasActivityExecution")

        if participation.participant_state_id is not None and \
                type(self.participant_state_service.get_participant_state(participation.participant_state_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(participation_id, participation.participant_state_id,
                                                        "hasParticipantState")

        return self.get_participation(participation_id)

    def get_participations(self):
        """
        Send request to graph api to get participations
        Returns:
            Result of request as list of participation objects
        """
        get_response = self.graph_api_service.get_nodes("Participation")

        participations = []

        for participation_node in get_response["nodes"]:
            properties = {'id': participation_node['id']}
            for property in participation_node["properties"]:
                if property["key"] == "age":
                    properties[property["key"]] = property["value"]
            participation = BasicParticipationOut(**properties)
            participations.append(participation)

        return ParticipationsOut(participations=participations)

    def get_participation(self, participation_id: int):
        """
        Send request to graph api to get given participation
        Args:
            participation_id (int): Id of participation
        Returns:
            Result of request as participation object
        """
        get_response = self.graph_api_service.get_node(participation_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participation_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Participation":
            return NotFoundByIdModel(id=participation_id, errors="Node not found.")

        participation = {'id': get_response['id'], 'relations': [],
                         'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] == "age":
                participation[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(participation_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == participation_id:
                participation['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                      name=relation["name"],
                                                                      relation_id=relation["id"]))
            else:
                participation['reversed_relations'].append(
                    RelationInformation(second_node_id=relation["start_node"],
                                        name=relation["name"],
                                        relation_id=relation["id"]))

        return ParticipationOut(**participation)

    def delete_participation(self, participation_id: int):
        """
        Send request to graph api to delete given participation
        Args:
            participation_id (int): Id of participation
        Returns:
            Result of request as participation object
        """
        get_response = self.get_participation(participation_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(participation_id)
        return get_response

    def update_participation_relationships(self, participation_id: int,
                                           participation: ParticipationIn):
        """
        Send request to graph api to update given participation
        Args:
            participation_id (int): Id of participation
            participation (ParticipationIn): Relationships to update
        Returns:
            Result of request as participation object
        """
        get_response = self.get_participation(participation_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if participation.activity_execution_id is not None and \
                type(self.activity_execution_service.get_activity_execution(participation.activity_execution_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(participation_id, participation.activity_execution_id,
                                                        "hasActivityExecution")

        if participation.participant_state_id is not None and \
                type(self.participant_state_service.get_participant_state(participation.participant_state_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(participation_id, participation.participant_state_id,
                                                        "hasParticipantState")

        return self.get_participation(participation_id)
