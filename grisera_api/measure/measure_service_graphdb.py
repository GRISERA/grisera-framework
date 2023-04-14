from graph_api_service import GraphApiService
from measure.measure_model import MeasurePropertyIn, BasicMeasureOut, \
    MeasuresOut, MeasureOut, MeasureIn, MeasureRelationIn
from measure.measure_service import MeasureService
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class MeasureServiceGraphDB(MeasureService):
    """
    Object to handle logic of measure requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_name_service (MeasureNameService): Service to manage measure name models
    """
    graph_api_service = GraphApiService()
    measure_name_service = MeasureNameServiceGraphDB()

    def save_measure(self, measure: MeasureIn, dataset_name: str):
        """
        Send request to graph api to create new measure

        Args:
            measure (MeasureIn): Measure to be added

        Returns:
            Result of request as measure object
        """
        node_response = self.graph_api_service.create_node("`Measure`", dataset_name)

        if node_response["errors"] is not None:
            return MeasureOut(**measure.dict(), errors=node_response["errors"])

        measure_id = node_response["id"]

        if measure.measure_name_id is not None and \
                type(self.measure_name_service.get_measure_name(measure.measure_name_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=measure_id,
                                                        end_node=measure.measure_name_id,
                                                        name="hasMeasureName",
                                                        dataset_name=dataset_name
                                                        )

        measure.measure_name_id = None
        self.graph_api_service.create_properties(measure_id, measure, dataset_name)

        return self.get_measure(measure_id, dataset_name)

    def get_measures(self, dataset_name: str):
        """
        Send request to graph api to get measures

        Returns:
            Result of request as list of measures objects
        """
        get_response = self.graph_api_service.get_nodes("`Measure`", dataset_name)

        measures = []

        for measure_node in get_response["nodes"]:
            properties = {'id': measure_node['id']}
            for property in measure_node["properties"]:
                if property["key"] in ["datatype", "range", "unit"]:
                    properties[property["key"]] = property["value"]

            measure = BasicMeasureOut(**properties)
            measures.append(measure)

        return MeasuresOut(measures=measures)

    def get_measure(self, measure_id: int, dataset_name: str):
        """
        Send request to graph api to get given measure

        Args:
            measure_id (int): Id of measure

        Returns:
            Result of request as measure object
        """
        get_response = self.graph_api_service.get_node(measure_id, dataset_name)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=measure_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Measure":
            return NotFoundByIdModel(id=measure_id, errors="Node not found.")

        measure = {'id': get_response['id'], 'relations': [],
                   'reversed_relations': []}
        for property in get_response["properties"]:
            if property["key"] in ["datatype", "range", "unit"]:
                measure[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(measure_id, dataset_name)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == measure_id:
                measure['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                name=relation["name"],
                                                                relation_id=relation["id"]))
            else:
                measure['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                         name=relation["name"],
                                                                         relation_id=relation["id"]))

        return MeasureOut(**measure)

    def delete_measure(self, measure_id: int, dataset_name: str):
        """
        Send request to graph api to delete given measure

        Args:
            measure_id (int): Id of measure

        Returns:
            Result of request as measure object
        """
        get_response = self.get_measure(measure_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(measure_id, dataset_name)
        return get_response

    def update_measure(self, measure_id: int, measure: MeasurePropertyIn, dataset_name: str):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int): Id of measure
            measure (MeasurePropertyIn): Properties to update

        Returns:
            Result of request as measure object
        """
        get_response = self.get_measure(measure_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node_properties(measure_id, dataset_name)
        self.graph_api_service.create_properties(measure_id, measure, dataset_name)

        measure_result = {"id": measure_id, "relations": get_response.relations,
                          "reversed_relations": get_response.reversed_relations}
        measure_result.update(measure.dict())

        return MeasureOut(**measure_result)

    def update_measure_relationships(self, measure_id: int,
                                     measure: MeasureRelationIn, dataset_name: str):
        """
        Send request to graph api to update given measure

        Args:
            measure_id (int): Id of measure
            measure (MeasureRelationIn): Relationships to update

        Returns:
            Result of request as measure object
        """
        get_response = self.get_measure(measure_id, dataset_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        if measure.measure_name_id is not None and \
                type(self.measure_name_service.get_measure_name(
                    measure.measure_name_id, dataset_name)) is not NotFoundByIdModel:
            self.graph_api_service.create_relationships(start_node=measure_id,
                                                        end_node=measure.measure_name_id,
                                                        name="hasMeasureName",
                                                        dataset_name=dataset_name)
        return self.get_measure(measure_id, dataset_name)
