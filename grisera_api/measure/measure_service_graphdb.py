from typing import Union

from ..graph_api_service import GraphApiService
from ..helpers import create_stub_from_response
from ..measure.measure_model import MeasurePropertyIn, BasicMeasureOut, \
    MeasuresOut, MeasureOut, MeasureIn, MeasureRelationIn
from ..measure.measure_service import MeasureService
from ..models.not_found_model import NotFoundByIdModel
from ..services import Services


class MeasureServiceGraphDB(MeasureService):
    """
    Object to handle logic of measure requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_name_service (MeasureNameService): Service to manage measure name models
    """
    graph_api_service = GraphApiService()

    def __init__(self):
        self.measure_name_service = Services().measure_name_service()
        self.time_series_service = Services().time_series_service()

    def save_measure(self, measure: MeasureIn):
        """
        Send request to graph api to create new measure

        Args:
            measure (MeasureIn): Measure to be added

        Returns:
            Result of request as measure object
        """
        node_response = self.graph_api_service.create_node("`Measure`")

        if node_response["errors"] is not None:
            return MeasureOut(**measure.dict(), errors=node_response["errors"])

        measure_id = node_response["id"]

        if measure.measure_name_id is not None and \
                type(self.measure_name_service.get_measure_name(measure.measure_name_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=measure_id,
                                                        end_node=measure.measure_name_id,
                                                        name="hasMeasureName")

        measure.measure_name_id = None
        self.graph_api_service.create_properties(measure_id, measure)

        return self.get_measure(measure_id)

    def get_measures(self):
        """
        Send request to graph api to get measures

        Returns:
            Result of request as list of measures objects
        """
        get_response = self.graph_api_service.get_nodes("`Measure`")

        measures = []

        for measure_node in get_response["nodes"]:
            properties = {'id': measure_node['id']}
            for property in measure_node["properties"]:
                if property["key"] in ["datatype", "range", "unit"]:
                    properties[property["key"]] = property["value"]

            measure = BasicMeasureOut(**properties)
            measures.append(measure)

        return MeasuresOut(measures=measures)

    def get_measure(self, measure_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get given measure

        Args:
            depth: (int): specifies how many related entities will be traversed to create the response
            measure_id (int | str): identity of measure

        Returns:
            Result of request as measure object
        """

        get_response = self.graph_api_service.get_node(measure_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=measure_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Measure":
            return NotFoundByIdModel(id=measure_id, errors="Node not found.")

        measure = create_stub_from_response(get_response)

        if depth != 0:
            measure["time_series"] = []
            measure["measure_name"] = None
            relations_response = self.graph_api_service.get_node_relationships(measure_id)

            for relation in relations_response["relationships"]:
                if relation["start_node"] == measure_id & relation["name"] == "hasMeasureName":
                    measure['measure_name'] = self.measure_name_service.get_measure_name(relation["end_node"], depth-1)
                else:
                    if relation["end_node"] == measure_id & relation["name"] == "hasMeasure":
                        measure['time_series'].append(self.time_series_service.get_time_series(relation["start_node"],
                                                                                               depth - 1))

            return MeasureOut(**measure)
        else:
            return BasicMeasureOut(**measure)

    def delete_measure(self, measure_id: Union[int, str]):
        """
        Send request to graph api to delete given measure

        Args:
            measure_id (int | str): identity of measure

        Returns:
            Result of request as measure object
        """
        get_response = self.get_measure(measure_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(measure_id)
        return get_response

    def update_measure(self, measure_id: Union[int, str], measure: MeasurePropertyIn):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int | str): identity of measure
            measure (MeasurePropertyIn): Properties to update

        Returns:
            Result of request as measure object
        """
        get_response = self.get_measure(measure_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(measure_id)
        self.graph_api_service.create_properties(measure_id, measure)

        measure_result = {"id": measure_id, "time_series": get_response.time_series,
                          "measure_name": get_response.measure_name}
        measure_result.update(measure.dict())

        return MeasureOut(**measure_result)

    def update_measure_relationships(self, measure_id: Union[int, str],
                                     measure: MeasureRelationIn):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int | str): identity of measure
            measure (MeasureRelationIn): Relationships to update

        Returns:
            Result of request as measure object
        """
        get_response = self.get_measure(measure_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if measure.measure_name_id is not None and \
                type(self.measure_name_service.get_measure_name(
                    measure.measure_name_id)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=measure_id,
                                                        end_node=measure.measure_name_id,
                                                        name="hasMeasureName")
        return self.get_measure(measure_id)
