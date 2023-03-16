from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from recording.recording_service import RecordingService
from recording.recording_model import RecordingPropertyIn, RecordingIn, BasicRecordingOut, RecordingOut, RecordingsOut
from models.not_found_model import NotFoundByIdModel


class RecordingServiceGraphDB(RecordingService):
    """
    Object to handle logic of recording requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    participation_service (ParticipationService): Service to send participation requests
    registered_channel_service(RegisteredChannelService): Service to send registered channel requests
    """
    graph_api_service = GraphApiService()

    def __init__(self, participation_service, registered_channel_service, observable_information_service):
        self.participation_service = participation_service()
        self.registered_channel_service = registered_channel_service()
        self.observation_information_service = observable_information_service()

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

    def get_recording(self, recording_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given recording
        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            recording_id (int | str): identity of recording
        Returns:
            Result of request as recording object
        """

        get_response = self.graph_api_service.get_node(recording_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=recording_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Recording":
            return NotFoundByIdModel(id=recording_id, errors="Node not found.")

        recording = create_stub_from_response(get_response)

        if depth != 0:
            recording["registered_channel"] = None
            recording["participation"] = None
            recording["observable_informations"] = []

            relations_response = self.graph_api_service.get_node_relationships(recording_id)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == recording_id & relation["name"] == "hasRegisteredChannel":
                    recording["registered_channel"] = self.registered_channel_service. \
                        get_registered_channel(relation["end_node"], depth - 1)
                else:
                    if relation["start_node"] == recording_id & relation["name"] == "hasParticipation":
                        recording["participation"] = self.participation_service. \
                            get_participation(relation["end_node"], depth - 1)
                    else:
                        if relation["end_node"] == recording_id & relation["name"] == "hasRecording":
                            recording["observable_informations"].append(self.participation_service.
                                                                        get_participation(relation["start_node"],
                                                                                          depth - 1))

            return RecordingOut(**recording)
        else:
            return BasicRecordingOut(**recording)

    def delete_recording(self, recording_id: Union[int, str]):
        """
        Send request to graph api to delete given recording
        Args:
            recording_id (int | str): identity of recording
        Returns:
            Result of request as recording object
        """
        get_response = self.get_recording(recording_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(recording_id)
        return get_response

    def update_recording(self, recording_id: Union[int, str], recording: RecordingPropertyIn):
        """
        Send request to graph api to update given participant state
        Args:
            recording_id (int | str): identity of participant state
            recording (RecordingPropertyIn): Properties to update
        Returns:
            Result of request as participant state object
        """
        get_response = self.get_recording(recording_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(recording_id)
        self.graph_api_service.create_properties(recording_id, recording)

        recording_result = {"id": recording_id, "registered_channel": get_response.registered_channel,
                            "participation": get_response.participation,
                            "observable_information": get_response.observable_informations}
        recording_result.update(recording.dict())

        return RecordingOut(**recording_result)

    def update_recording_relationships(self, recording_id: Union[int, str],
                                       recording: RecordingIn):
        """
        Send request to graph api to update given recording
        Args:
            recording_id (int | str): identity of recording
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
