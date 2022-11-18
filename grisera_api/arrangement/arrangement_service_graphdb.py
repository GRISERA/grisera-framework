from arrangement.arrangement_service import ArrangementService
from graph_api_service import GraphApiService
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, ArrangementsOut, BasicArrangementOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class ArrangementServiceGraphDB(ArrangementService):
    """
    Object to handle logic of arrangement requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_arrangement(self, arrangement: ArrangementIn):
        """
        Send request to graph api to create new arrangement

        Args:
            arrangement (ArrangementIn): Arrangement to be added

        Returns:
            Result of request as arrangement object
        """

        node_response = self.graph_api_service.create_node("Arrangement")

        if node_response["errors"] is not None:
            return ArrangementOut(arrangement_type=arrangement.arrangement_type,
                                  arrangement_distance=arrangement.arrangement_distance, errors=node_response["errors"])

        arrangement_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(arrangement_id, arrangement)
        if properties_response["errors"] is not None:
            return ArrangementOut(arrangement_type=arrangement.arrangement_type,
                                  arrangement_distance=arrangement.arrangement_distance,
                                  errors=properties_response["errors"])

        return ArrangementOut(arrangement_type=arrangement.arrangement_type,
                              arrangement_distance=arrangement.arrangement_distance, id=arrangement_id)

    def get_arrangements(self):
        """
        Send request to graph api to get all arrangements

        Returns:
            Result of request as list of arrangement objects
        """
        get_response = self.graph_api_service.get_nodes("Arrangement")
        if get_response["errors"] is not None:
            return ArrangementsOut(errors=get_response["errors"])

        arrangements = []
        for arrangement in get_response["nodes"]:
            if arrangement["properties"][0]["key"] == 'arrangement_distance':
                arrangements.append(BasicArrangementOut(id=arrangement["id"],
                                                        arrangement_type=arrangement["properties"][1]["value"],
                                                        arrangement_distance=arrangement["properties"][0]["value"]))
            else:
                arrangements.append(BasicArrangementOut(id=arrangement["id"],
                                                        arrangement_type=arrangement["properties"][0]["value"],
                                                        arrangement_distance=None))

        return ArrangementsOut(arrangements=arrangements)

    def get_arrangement(self, arrangement_id: int):
        """
        Send request to graph api to get given arrangement

        Args:
            arrangement_id (int): Id of arrangement

        Returns:
            Result of request as arrangement object
        """
        get_response = self.graph_api_service.get_node(arrangement_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=arrangement_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Arrangement":
            return NotFoundByIdModel(id=arrangement_id, errors="Node not found.")

        arrangement = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            arrangement[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(arrangement_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == arrangement_id:
                arrangement['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                    name=relation["name"], relation_id=relation["id"]))
            else:
                arrangement['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                             name=relation["name"],
                                                                             relation_id=relation["id"]))

        return ArrangementOut(**arrangement)
