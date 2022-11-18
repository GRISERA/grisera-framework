from graph_api_service import GraphApiService
from measure.measure_service import MeasureService
from observable_information.observable_information_service import ObservableInformationService
from time_series.time_series_model import TimeSeriesPropertyIn, BasicTimeSeriesOut, \
    TimeSeriesNodesOut, TimeSeriesOut, TimeSeriesIn, TimeSeriesRelationIn
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class TimeSeriesService:
    """
    Object to handle logic of time series requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        measure_service (MeasureService): Service to manage measure models
        observable_information_service (ObservableInformationService): Service to manage observable information models
    """
    graph_api_service = GraphApiService()
    measure_service = MeasureService()
    observable_information_service = ObservableInformationService()

    def save_time_series(self, time_series: TimeSeriesIn):
        """
        Send request to graph api to create new time series

        Args:
            time_series (TimeSeriesIn): Time series to be added

        Returns:
            Result of request as time series object
        """
        print("save_time_series not implemented yet")

    def get_time_series_nodes(self):
        """
        Send request to graph api to get time series nodes

        Returns:
            Result of request as list of time series nodes objects
        """
        print("get_time_series_nodes not implemented yet")

    def get_time_series(self, time_series_id: int):
        """
        Send request to graph api to get given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        print("get_time_series not implemented yet")

    def delete_time_series(self, time_series_id: int):
        """
        Send request to graph api to delete given time series

        Args:
            time_series_id (int): Id of time series

        Returns:
            Result of request as time series object
        """
        print("delete_time_series not implemented yet")

    def update_time_series(self, time_series_id: int, time_series: TimeSeriesPropertyIn):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesPropertyIn): Properties to update

        Returns:
            Result of request as time series object
        """
        print("update_time_series not implemented yet")

    def update_time_series_relationships(self, time_series_id: int,
                                               time_series: TimeSeriesRelationIn):
        """
        Send request to graph api to update given time series

        Args:
            time_series_id (int): Id of time series
            time_series (TimeSeriesRelationIn): Relationships to update

        Returns:
            Result of request as time series object
        """
        print("update_time_series_relationships not implemented yet")
