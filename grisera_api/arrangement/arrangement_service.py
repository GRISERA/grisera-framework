from graph_api_service import GraphApiService
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, ArrangementsOut, BasicArrangementOut


class ArrangementService:
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
