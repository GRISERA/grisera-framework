from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum
from property.property_model import PropertyIn
from models.relation_information_model import RelationInformation


class Type(str, Enum):
    """
    Types of time series

    Attributes:
        epoch (str): Epoch signal
        irregularly_spaced (str): Irregularly spaced signal
        regularly_spaced (str): Regularly spaced signal
        timestamp (str): Timestamp signal
    """
    epoch = "Epoch"
    irregularly_spaced = "Irregularly spaced"
    regularly_spaced = "Regularly spaced"
    timestamp = "Timestamp"


class TimeSeriesPropertyIn(BaseModel):
    """
    Model of time series to acquire from client

    Attributes:
        type (Type): Type of the signal
        source(str): TimeSeries source
        additional_properties (Optional[List[PropertyIn]]): Additional properties for signal
    """
    type: Type
    source: str
    additional_properties: Optional[List[PropertyIn]]


class TimeSeriesRelationIn(BaseModel):
    """
    Model of time series relations to acquire from client

    Attributes:
        observable_information_id (Optional[int]): Id of observable information
        measure_id (Optional[int]): Id of measure
    """
    observable_information_id: Optional[int]
    measure_id: Optional[int]


class TimeSeriesIn(TimeSeriesPropertyIn, TimeSeriesRelationIn):
    """
    Full model of time series to acquire from client
    """


class BasicTimeSeriesOut(TimeSeriesPropertyIn):
    """
    Basic model of time series

    Attributes:
        id (Optional[int]): Id of time series returned from graph api
    """
    id: Optional[int]


class TimeSeriesOut(BasicTimeSeriesOut):
    """
    Model of time series with relations to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in time series node
        reversed_relations (List[RelationInformation]): List of relations ending in time series node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class TimeSeriesNodesOut(BaseModel):
    """
    Model of time series nodes to send to client as a result of request

    Attributes:
        time_series_nodes (List[BasicTimeSeriesOut]): Time series nodes from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    time_series_nodes: List[BasicTimeSeriesOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
