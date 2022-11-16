from graph_api_service import GraphApiService
from participation.participation_service import ParticipationService
from registered_channel.registered_channel_service import RegisteredChannelService
from recording.recording_model import RecordingPropertyIn, RecordingRelationIn, RecordingIn, BasicRecordingOut, RecordingOut, RecordingsOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class RecordingServiceGraphDB:
    """
    Object to handle logic of recording requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    participation_service (ParticipationService): Service to send participation requests
    registered_channel_service(RegisteredChannelService): Service to send registered channel requests
    """
    graph_api_service = GraphApiService()
    participation_service = ParticipationService()
    registered_channel_service = RegisteredChannelService()

    def save_recording(self, recording: RecordingIn):
        """
        Send request to graph api to create new recording node

        Args:
            recording (RecordingIn): Recording to be added

        Returns:
            Result of request as recording object
        """
        node_response = self.graph_api_service.create_node("Recording")

        if node_response["errors"] is not None:
            return RecordingOut(**recording.dict(), errors=node_response["errors"])

        recording_id = node_response["id"]

        if recording.participation_id is not None and \
                type(self.participation_service.get_participation(recording.participation_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=recording_id,
                                                        end_node=recording.participation_id,
                                                        name="hasParticipation")
        if recording.registered_channel_id is not None and \
                type(self.registered_channel_service.get_registered_channel(recording.registered_channel_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=recording_id,
                                                        end_node=recording.registered_channel_id,
                                                        name="hasRegisteredChannel")
        recording.participation_id = recording.registered_channel_id = None
        self.graph_api_service.create_properties(recording_id, recording)
        
        return self.get_recording(recording_id)

    def get_recordings(self):
        """
        Send request to graph api to get recordings
        Returns:
            Result of request as list of recordings objects
        """
        get_response = self.graph_api_service.get_nodes("Recording")

        recordings = []

        for recording_node in get_response["nodes"]:
            properties = {'id': recording_node['id'], 'additional_properties': []}
            for property in recording_node["properties"]:
                properties['additional_properties'].append({'key': property['key'], 'value': property['value']})
            recording = BasicRecordingOut(**properties)
            recordings.append(recording)

        return RecordingsOut(recordings=recordings)

    def get_recording(self, recording_id: int):
        """
        Send request to graph api to get given recording
        Args:
            recording_id (int): Id of recording
        Returns:
            Result of request as recording object
        """
        get_response = self.graph_api_service.get_node(recording_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=recording_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Recording":
            return NotFoundByIdModel(id=recording_id, errors="Node not found.")

        recording = {'id': get_response['id'], 'additional_properties': [], 'relations': [],
                     'reversed_relations': []}

        for property in get_response["properties"]:
            recording['additional_properties'].append({'key': property['key'], 'value': property['value']})

        relations_response = self.graph_api_service.get_node_relationships(recording_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == recording_id:
                recording['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                  name=relation["name"],
                                                                  relation_id=relation["id"]))
            else:
                recording['reversed_relations'].append(
                    RelationInformation(second_node_id=relation["start_node"],
                                        name=relation["name"],
                                        relation_id=relation["id"]))

        return RecordingOut(**recording)

    def delete_recording(self, recording_id: int):
        """
        Send request to graph api to delete given recording
        Args:
            recording_id (int): Id of recording
        Returns:
            Result of request as recording object
        """
        get_response = self.get_recording(recording_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(recording_id)
        return get_response

    def update_recording(self, recording_id: int, recording: RecordingPropertyIn):
        """
        Send request to graph api to update given participant state
        Args:
            recording_id (int): Id of participant state
            recording (RecordingPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        get_response = self.get_recording(recording_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(recording_id)
        self.graph_api_service.create_properties(recording_id, recording)

        recording_result = {"id": recording_id, "relations": get_response.relations,
                            "reversed_relations": get_response.reversed_relations}
        recording_result.update(recording.dict())

        return RecordingOut(**recording_result)
    
    def update_recording_relationships(self, recording_id: int,
                                       recording: RecordingIn):
        """
        Send request to graph api to update given recording
        Args:
            recording_id (int): Id of recording
            recording (RecordingIn): Relationships to update
        Returns:
            Result of request as recording object
        """
        get_response = self.get_recording(recording_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if recording.participation_id is not None and \
                type(self.participation_service.get_participation(recording.participation_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=recording_id,
                                                        end_node=recording.participation_id,
                                                        name="hasParticipation")
        if recording.registered_channel_id is not None and \
                type(self.registered_channel_service.get_registered_channel(recording.registered_channel_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=recording_id,
                                                        end_node=recording.registered_channel_id,
                                                        name="hasRegisteredChannel")

        return self.get_recording(recording_id)
