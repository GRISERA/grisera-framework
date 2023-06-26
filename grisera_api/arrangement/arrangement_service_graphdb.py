from typing import Union

from activity_execution.activity_execution_service import ActivityExecutionService
from arrangement.arrangement_service import ArrangementService
from graph_api_service import GraphApiService
from arrangement.arrangement_model import ArrangementIn, ArrangementOut, ArrangementsOut, BasicArrangementOut
from helpers import create_stub_from_response
from models.not_found_model import NotFoundByIdModel


class ArrangementServiceGraphDB(ArrangementService):
    """
    Object to handle logic of arrangement requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.activity_execution_service: ActivityExecutionService = None

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

    def get_arrangement(self, arrangement_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given arrangement

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            arrangement_id (int | str): identity of arrangement

        Returns:
            Result of request as arrangement object
        """
        get_response = self.graph_api_service.get_node(arrangement_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=arrangement_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Arrangement":
            return NotFoundByIdModel(id=arrangement_id, errors="Node not found.")

        arrangement = create_stub_from_response(get_response, properties=['arrangement_type', 'arrangement_distance'])

        if depth != 0:
            arrangement["activity_executions"] = []

            relations_response = self.graph_api_service.get_node_relationships(arrangement_id)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == arrangement_id & relation["name"] == "hasArrangement":
                    arrangement['activity_executions'].append(
                        self.activity_execution_service.get_activity_execution(relation["start_node"], depth - 1))

            return ArrangementOut(**arrangement)
        else:
            return BasicArrangementOut(**arrangement)
