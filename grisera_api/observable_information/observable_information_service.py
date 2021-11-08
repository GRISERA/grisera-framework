from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut
from modality.modality_service import ModalityService
from live_activity.live_activity_service import LiveActivityService
from recording.recording_service import RecordingService


class ObservableInformationService:
    """
    Object to handle logic of observable information requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    modality_service (ModalityService): Service used to communicate with Modality
    live_activity_service (LiveActivityService): Service used to communicate with Live Activity
    recording_service (RecordingService): Service used to communicate with Recording
    """
    graph_api_service = GraphApiService()
    modality_service = ModalityService()
    live_activity_service = LiveActivityService()
    recording_service = RecordingService()

    def save_observable_information(self, observable_information: ObservableInformationIn):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added

        Returns:
            Result of request as observable information object
        """
        node_response = self.graph_api_service.create_node("`Observable information`")

        if node_response["errors"] is not None:
            return ObservableInformationOut(modality=observable_information.modality,
                                            live_activity=observable_information.live_activity,
                                            errors=node_response["errors"])

        observable_information_id = node_response["id"]

        if observable_information.modality_id is not None and \
                type(self.modality_service.get_modality(observable_information.modality_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.modality_id, name="hasModality")

        if observable_information.live_activity_id is not None and \
                type(self.live_activity_service.get_live_activity(
                    observable_information.live_activity_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.live_activity_id,
                                                        name="hasLiveActivity")

        if observable_information.recording_id is not None and \
                type(
                    self.recording_service.get_recording(observable_information.recording_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.recording_id,
                                                        name="hasRecording")

        return self.get_observable_information(observable_information_id)

    def get_observable_informations(self):
        """
        Send request to graph api to get observable information
        Returns:
            Result of request as list of observable information objects
        """
        get_response = self.graph_api_service.get_nodes("`Observable Information`")

        observable_informations = []

        for observable_information_node in get_response["nodes"]:
            properties = {'id': observable_information_node['id']}
            for property in observable_information_node["properties"]:
                if property["key"] == "age":
                    properties[property["key"]] = property["value"]
            observable_information = BasicObservableInformationOut(**properties)
            observable_informations.append(observable_information)

        return ObservableInformationsOut(observable_informations=observable_informations)

    def get_observable_information(self, observable_information_id: int):
        """
        Send request to graph api to get given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        get_response = self.graph_api_service.get_node(observable_information_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=observable_information_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Observable Information":
            return NotFoundByIdModel(id=observable_information_id, errors="Node not found.")

        observable_information = {'id': get_response['id'], 'relations': [],
                                  'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] == "age":
                observable_information[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(observable_information_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == observable_information_id:
                observable_information['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                               name=relation["name"],
                                                                               relation_id=relation["id"]))
            else:
                observable_information['reversed_relations'].append(
                    RelationInformation(second_node_id=relation["start_node"],
                                        name=relation["name"],
                                        relation_id=relation["id"]))

        return ObservableInformationOut(**observable_information)

    def delete_observable_information(self, observable_information_id: int):
        """
        Send request to graph api to delete given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        get_response = self.get_observable_information(observable_information_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(observable_information_id)
        return get_response

    def update_observable_information_relationships(self, observable_information_id: int,
                                                    observable_information: ObservableInformationIn):
        """
        Send request to graph api to update given observable information
        Args:
            observable_information_id (int): Id of observable information
            observable_information (ObservableInformationIn): Relationships to update
        Returns:
            Result of request as observable information object
        """
        get_response = self.get_observable_information(observable_information_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if observable_information.channel_id is not None and \
                type(self.channel_service.get_channel(observable_information.channel_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.channel_id,
                                                        name="hasChannel")
        if observable_information.registered_data_id is not None and \
                type(self.registered_data_service.get_registered_data(observable_information.registered_data_id)) \
                is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.registered_data_id,
                                                        name="hasRegisteredData")

        return self.get_observable_information(observable_information_id)
