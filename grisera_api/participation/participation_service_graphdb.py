from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from participation.participation_model import ParticipationIn, ParticipationOut, ParticipationsOut, \
    BasicParticipationOut
from models.not_found_model import NotFoundByIdModel
from participation.participation_service import ParticipationService


class ParticipationServiceGraphDB(ParticipationService):
    """
    Object to handle logic of participation requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    activity_execution_service (ActivityExecutionService): Service to send activity execution requests
    participant_state_service (ParticipantStateService): Service to send participant state requests
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.activity_execution_service = None
        self.participant_state_service = None
        self.recording_service = None

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
            self.graph_api_service.create_relationships(start_node=participation_id,
                                                        end_node=participation.activity_execution_id,
                                                        name="hasActivityExecution")

        if participation.participant_state_id is not None and \
                type(self.participant_state_service.get_participant_state(participation.participant_state_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participation_id,
                                                        end_node=participation.participant_state_id,
                                                        name="hasParticipantState")

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
            participation = BasicParticipationOut(**properties)
            participations.append(participation)

        return ParticipationsOut(participations=participations)

    def get_participation(self, participation_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given participation
        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            participation_id (int | str): identity of participation
        Returns:
            Result of request as participation object
        """
        get_response = self.graph_api_service.get_node(participation_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=participation_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Participation":
            return NotFoundByIdModel(id=participation_id, errors="Node not found.")

        participation = create_stub_from_response(get_response)

        if depth != 0:
            participation["participant_state"] = None
            participation['activity_execution'] = None
            participation['recordings'] = []

            relations_response = self.graph_api_service.get_node_relationships(participation_id)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == participation_id & relation["name"] == "hasParticipantState":
                    participation["participant_state"] = self.participant_state_service. \
                        get_participant_state(relation["end_node"], depth - 1)
                else:
                    if relation["start_node"] == participation_id & relation["name"] == "hasActivityExecution":
                        participation['activity_execution']. \
                            append(self.activity_execution_service.
                                   get_activity_execution(relation["end_node"], depth - 1))
                    else:
                        if relation["end_node"] == participation_id & relation["name"] == "hasParticipation":
                            participation['recordings'].append(
                                self.recording_service.get_recording(relation["end_node"], depth - 1))

            return ParticipationOut(**participation)
        else:
            return BasicParticipationOut(**participation)

    def delete_participation(self, participation_id: Union[int, str]):
        """
        Send request to graph api to delete given participation
        Args:
            participation_id (int | str): identity of participation
        Returns:
            Result of request as participation object
        """
        get_response = self.get_participation(participation_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(participation_id)
        return get_response

    def update_participation_relationships(self, participation_id: Union[int, str],
                                           participation: ParticipationIn):
        """
        Send request to graph api to update given participation relationships
        Args:
            participation_id (int | str): identity of participation
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
            self.graph_api_service.create_relationships(start_node=participation_id,
                                                        end_node=participation.activity_execution_id,
                                                        name="hasActivityExecution")

        if participation.participant_state_id is not None and \
                type(self.participant_state_service.get_participant_state(participation.participant_state_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=participation_id,
                                                        end_node=participation.participant_state_id,
                                                        name="hasParticipantState")

        return self.get_participation(participation_id)
