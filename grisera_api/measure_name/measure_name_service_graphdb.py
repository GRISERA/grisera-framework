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

    def save_measure_name(self, measure_name: MeasureNameIn, dataset_name: str):
        """
        Send request to graph api to create new measure name

        Args:
            measure_name (MeasureNameIn): Measure name to be added
            dataset_name (str): name of dataset

        Returns:
            Result of request as measure name object
        """
        create_response = self.graph_api_service.create_node("`Measure Name`", dataset_name)

        if create_response["errors"] is not None:
            return MeasureNameOut(name=measure_name.name, type=measure_name.type, errors=create_response["errors"])

        measure_name_id = create_response["id"]
        properties_response = self.graph_api_service.create_properties(measure_name_id, measure_name, dataset_name)
        if properties_response["errors"] is not None:
            return MeasureNameOut(name=measure_name.name, type=measure_name.type, errors=properties_response["errors"])

        return MeasureNameOut(name=measure_name.name, type=measure_name.type, id=measure_name_id)

    def get_measure_names(self, dataset_name: str):
        """
        Send request to graph api to get all measure names

        Args:
            dataset_name (str): name of dataset

        Returns:
            Result of request as list of measure name objects
        """
        get_response = self.graph_api_service.get_nodes("`Measure Name`", dataset_name)
        if get_response["errors"] is not None:
            return MeasureNamesOut(errors=get_response["errors"])
        measure_names = [BasicMeasureNameOut(id=measure_name["id"],
                                             **{measure_name["properties"][0]["key"]:
                                                measure_name["properties"][0]["value"],
                                                measure_name["properties"][1]["key"]:
                                                    measure_name["properties"][1]["value"]})
                         for measure_name in get_response["nodes"]]

        return MeasureNamesOut(measure_names=measure_names)

    def get_measure_name(self, measure_name_id: Union[int, str], dataset_name: str, depth: int = 0):
        """
        Send request to graph api to get given measure name

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            measure_name_id (int | str): identity of measure name
            dataset_name (str): name of dataset
        Returns:
            Result of request as measure name object
        """
        get_response = self.graph_api_service.get_node(measure_name_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=measure_name_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Measure Name":
            return NotFoundByIdModel(id=measure_name_id, errors="Node not found.")

        measure_name = create_stub_from_response(get_response, properties=['name', 'type'])

        if depth != 0:
            measure_name["measures"] = []
            relations_response = self.graph_api_service.get_node_relationships(measure_name_id, dataset_name)

            for relation in relations_response["relationships"]:
                if relation["end_node"] == measure_name_id & relation["name"] == "hasMeasureName":
                    measure_name['measures'].append(self.measure_service.
                                                    get_measure(relation["start_node"], depth - 1))

            return MeasureNameOut(**measure_name)
        else:
            return BasicMeasureNameOut(**measure_name)

    def delete_measure_name(self, measure_name_id: int, dataset_name: str):
        """
        Send request to graph api to delete given measure_name
        Args:
            measure_name_id (int): Id of measure_name
            dataset_name (str): name of dataset
        Returns:
            Result of request as measure_name object
        """
        get_response = self.get_measure_name(measure_name_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(measure_name_id, dataset_name)
        return get_response

    def update_measure_name(self, measure_name_id: int, measure_name: MeasureNameIn, dataset_name: str):
        """
        Send request to graph api to update given measure_name
        Args:
            measure_name_id (int): Id of measure_name
            measure_name (MeasureNameIn): Measure_name to be updated
            dataset_name (str): name of dataset
        Returns:
            Result of request as measure_name object
        """
        get_response = self.get_measure_name(measure_name_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        self.graph_api_service.delete_node_properties(measure_name_id, dataset_name)
        self.graph_api_service.create_properties(measure_name_id, measure_name, dataset_name)

        measure_name_result = {'id': measure_name_id, 'relations': get_response.relations,
                             'reversed_relations': get_response.reversed_relations}
        measure_name_result.update(get_response.dict())

        return MeasureNameOut(**measure_name_result)
