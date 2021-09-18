from graph_api_service import GraphApiService
from time_series.time_series_model import TimeSeriesIn, TimeSeriesOut


class TimeSeriesService:
    """
    Object to handle logic of time_series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_time_series(self, time_series: TimeSeriesIn):
        """
        Send request to graph api to create new time_series

        Args:
            time_series (TimeSeriesIn): TimeSeries to be added

        Returns:
            Result of request as time_series object
        """
        node_response_time_series = self.graph_api_service.create_node("TimeSeries")

        if node_response_time_series["errors"] is not None:
            return TimeSeriesOut(type=time_series.type, source=time_series.source,
                                 observable_information_id=time_series.observable_information_id,
                                 measure_id=time_series.measure_id,
                                 additional_properties=time_series.additional_properties,
                                 errors=node_response_time_series["errors"])

        time_series_id = node_response_time_series["id"]
        properties_response = self.graph_api_service.create_properties(time_series_id, time_series)
        if properties_response["errors"] is not None:
            return TimeSeriesOut(type=time_series.type, source=time_series.source,
                                 observable_information_id=time_series.observable_information_id,
                                 measure_id=time_series.measure_id,
                                 additional_properties=time_series.additional_properties,
                                 errors=properties_response["errors"])

        self.graph_api_service.create_relationships(time_series_id, time_series.observable_information_id,
                                                    "hasObservableInformation")

        self.graph_api_service.create_relationships(time_series_id, time_series.measure_id,
                                                    "hasMeasure")

        return TimeSeriesOut(type=time_series.type, source=time_series.source,
                             observable_information_id=time_series.observable_information_id,
                             measure_id=time_series.measure_id, id=time_series_id,
                             additional_properties=time_series.additional_properties)
