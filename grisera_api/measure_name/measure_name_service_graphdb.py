from typing import Union

from graph_api_service import GraphApiService
from helpers import create_stub_from_response
from measure.measure_service import MeasureService
from measure_name.measure_name_model import MeasureNameIn, MeasureNameOut, MeasureNamesOut, BasicMeasureNameOut
from measure_name.measure_name_service import MeasureNameService
from models.not_found_model import NotFoundByIdModel


class MeasureNameServiceGraphDB(MeasureNameService):
    """
    Object to handle logic of measure name requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.measure_service: MeasureService = None

    def save_measure_name(self, measure_name: MeasureNameIn):
        """
        Send request to graph api to create new measure name

        Args:
            measure_name (MeasureNameIn): Measure name to be added

        Returns:
            Result of request as measure name object
        """
        create_response = self.graph_api_service.create_node("`Measure Name`")

        if create_response["errors"] is not None:
            return MeasureNameOut(name=measure_name.name, type=measure_name.type, errors=create_response["errors"])

        measure_name_id = create_response["id"]
        properties_response = self.graph_api_service.create_properties(measure_name_id, measure_name)
        if properties_response["errors"] is not None:
            return MeasureNameOut(name=measure_name.name, type=measure_name.type, errors=properties_response["errors"])

        return MeasureNameOut(name=measure_name.name, type=measure_name.type, id=measure_name_id)

    def get_measure_names(self):
        """
        Send request to graph api to get all measure names

        Returns:
            Result of request as list of measure name objects
        """
        get_response = self.graph_api_service.get_nodes("`Measure Name`")
        if get_response["errors"] is not None:
            return MeasureNamesOut(errors=get_response["errors"])
        measure_names = [BasicMeasureNameOut(id=measure_name["id"],
                                             **{measure_name["properties"][0]["key"]:
                                                measure_name["properties"][0]["value"],
                                                measure_name["properties"][1]["key"]:
                                                    measure_name["properties"][1]["value"]})
                         for measure_name in get_response["nodes"]]

        return MeasureNamesOut(measure_names=measure_names)

    def get_measure_name(self, measure_name_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given measure name

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            measure_name_id (int | str): identity of measure name

        Returns:
            Result of request as measure name object
        """
        get_response = self.graph_api_service.get_node(measure_name_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=measure_name_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Measure Name":
            return NotFoundByIdModel(id=measure_name_id, errors="Node not found.")

        measure_name = create_stub_from_response(get_response, properties=['name', 'type'])

        if depth != 0:
            measure_name["measures"] = []
            relations_response = self.graph_api_service.get_node_relationships(measure_name_id)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == measure_name_id & relation["name"] == "hasMeasureName":
                    measure_name['measures'].append(self.measure_service.
                                                    get_measure(relation["start_node"], depth - 1))

            return MeasureNameOut(**measure_name)
        else:
            return BasicMeasureNameOut(**measure_name)
