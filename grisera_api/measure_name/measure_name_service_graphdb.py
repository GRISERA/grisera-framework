from graph_api_service import GraphApiService
from measure_name.measure_name_model import MeasureNameIn, MeasureNameOut, MeasureNamesOut, BasicMeasureNameOut
from measure_name.measure_name_service import MeasureNameService
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class MeasureNameServiceGraphDB(MeasureNameService):
    """
    Object to handle logic of measure name requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

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

    def get_measure_name(self, measure_name_id: int):
        """
        Send request to graph api to get given measure name

        Args:
        measure_name_id (int): Id of measure name

        Returns:
            Result of request as measure name object
        """
        get_response = self.graph_api_service.get_node(measure_name_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=measure_name_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Measure Name":
            return NotFoundByIdModel(id=measure_name_id, errors="Node not found.")

        measure_name = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            measure_name[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(measure_name_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == measure_name_id:
                measure_name['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                     name=relation["name"],
                                                                     relation_id=relation["id"]))
            else:
                measure_name['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                              name=relation["name"],
                                                                              relation_id=relation["id"]))

        return MeasureNameOut(**measure_name)
