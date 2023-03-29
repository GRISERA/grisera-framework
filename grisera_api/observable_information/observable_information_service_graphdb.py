from graph_api_service import GraphApiService
from observable_information.observable_information_model import ObservableInformationIn, ObservableInformationOut, \
    BasicObservableInformationOut, ObservableInformationsOut
from modality.modality_service_graphdb import ModalityServiceGraphDB
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from observable_information.observable_information_service import ObservableInformationService
from recording.recording_service_graphdb import RecordingServiceGraphDB
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ObservableInformationServiceGraphDB(ObservableInformationService):
    """
    Object to handle logic of observable information requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    modality_service (ModalityService): Service used to communicate with Modality
    life_activity_service (LifeActivityService): Service used to communicate with Life Activity
    recording_service (RecordingService): Service used to communicate with Recording
    """
    graph_api_service = GraphApiService()
    modality_service = ModalityServiceGraphDB()
    life_activity_service = LifeActivityServiceGraphDB()
    recording_service = RecordingServiceGraphDB()

    def save_observable_information(self, observable_information: ObservableInformationIn, database_name: str):
        """
        Send request to graph api to create new observable information

        Args:
            observable_information (ObservableInformationIn): Observable information to be added

        Returns:
            Result of request as observable information object
        """
        node_response = self.graph_api_service.create_node("`Observable Information`", database_name)

        if node_response["errors"] is not None:
            return ObservableInformationOut(errors=node_response["errors"])

        observable_information_id = node_response["id"]

        if observable_information.modality_id is not None and \
                type(self.modality_service.get_modality(observable_information.modality_id,database_name=database_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.modality_id, name="hasModality",
                                                        database_name=database_name)

        if observable_information.life_activity_id is not None and \
                type(self.life_activity_service.get_life_activity(
                    observable_information.life_activity_id, database_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.life_activity_id,
                                                        name="hasLifeActivity",
                                                        database_name=database_name)

        if observable_information.recording_id is not None and \
                type(
                    self.recording_service.get_recording(observable_information.recording_id, database_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.recording_id,
                                                        name="hasRecording",
                                                        database_name=database_name)

        return self.get_observable_information(observable_information_id, database_name)

    def get_observable_informations(self, database_name: str):
        """
        Send request to graph api to get observable information
        Returns:
            Result of request as list of observable information objects
        """
        get_response = self.graph_api_service.get_nodes("`Observable Information`", database_name)

        observable_informations = []

        for observable_information_node in get_response["nodes"]:
            properties = {'id': observable_information_node['id']}
            observable_information = BasicObservableInformationOut(**properties)
            observable_informations.append(observable_information)

        return ObservableInformationsOut(observable_informations=observable_informations)

    def get_observable_information(self, observable_information_id: int, database_name: str):
        """
        Send request to graph api to get given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        get_response = self.graph_api_service.get_node(observable_information_id, database_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=observable_information_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Observable Information":
            return NotFoundByIdModel(id=observable_information_id, errors="Node not found.")

        observable_information = {'id': get_response['id'], 'relations': [],
                                  'reversed_relations': []}

        relations_response = self.graph_api_service.get_node_relationships(observable_information_id, database_name)

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

    def delete_observable_information(self, observable_information_id: int, database_name: str):
        """
        Send request to graph api to delete given observable information
        Args:
            observable_information_id (int): Id of observable information
        Returns:
            Result of request as observable information object
        """
        get_response = self.get_observable_information(observable_information_id, database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(observable_information_id, database_name)
        return get_response

    def update_observable_information_relationships(self, observable_information_id: int,
                                                    observable_information: ObservableInformationIn, database_name: str):
        """
        Send request to graph api to update given observable information
        Args:
            observable_information_id (int): Id of observable information
            observable_information (ObservableInformationIn): Relationships to update
        Returns:
            Result of request as observable information object
        """
        get_response = self.get_observable_information(observable_information_id, database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if observable_information.modality_id is not None and \
                type(self.modality_service.get_modality(observable_information.modality_id, database_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.modality_id, name="hasModality",
                                                        database_name=database_name)

        if observable_information.life_activity_id is not None and \
                type(self.life_activity_service.get_life_activity(
                    observable_information.life_activity_id, database_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.life_activity_id,
                                                        name="hasLifeActivity",
                                                        database_name=database_name)

        if observable_information.recording_id is not None and \
                type(
                    self.recording_service.get_recording(observable_information.recording_id, database_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=observable_information_id,
                                                        end_node=observable_information.recording_id,
                                                        name="hasRecording",
                                                        database_name=database_name)

        return self.get_observable_information(observable_information_id, database_name)
