from graph_api_service import GraphApiService
from measure.measure_model import MeasureIn, MeasureOut
from measure_name.measure_name_service import MeasureNameService


class MeasureService:
    """
    Object to handle logic of measures requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_name_service (MeasureNameService): Service to send measure name requests
    """
    graph_api_service = GraphApiService()
    measure_name_service = MeasureNameService()

    def save_measure(self, measure: MeasureIn):
        """
        Send request to graph api to create new measure

        Args:
            measure (MeasureIn): Measure to be added

        Returns:
            Result of request as measure object
        """
        node_response = self.graph_api_service.create_node("Measure")

        if node_response["errors"] is not None:
            return MeasureOut(measure_name=measure.measure_name, data_type=measure.data_type,
                           range=measure.range, errors=node_response["errors"])
        measure_id = node_response["id"]

        measure_names = self.measure_name_service.get_measure_names().measure_names
        measure_name_id, measure_name = next((measure_name.id, measure_name.name) for measure_name in measure_names
                                         if measure_name.name == measure.measure_name)
        self.graph_api_service.create_relationships(start_node=measure_id,
                                                    end_node=measure_name_id,
                                                    name="hasMeasureName")
        measure.measure_name = None
        properties_response = self.graph_api_service.create_properties(measure_id, measure)

        return MeasureOut(measure_name=measure_name, data_type=measure.data_type,
                          range=measure.range, id=measure_id)
