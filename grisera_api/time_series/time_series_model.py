from enum import Enum
from typing import Optional, Any, List, Union

from pydantic import BaseModel

from models.relation_information_model import RelationInformation
from property.property_model import PropertyIn


class TransformationType(str, Enum):
    """
    The type of transformation
    """
    RESAMPLE_NEAREST = "resample_nearest"
    QUADRANTS = "quadrants"


class TimestampNodesIn(BaseModel):
    """
    Model of timestamp node
    Attributes:
        timestamp (int): Timestamp of signal measure in milliseconds
    """
    timestamp: int


class SignalValueNodesIn(BaseModel):
    """
    Model of signal value node
    Attributes:
        value (Union[str, float]): Value of signal
    """
    value: Union[str, float]


class SignalIn(BaseModel):
    """
    Model of signal to acquire from client
    Attributes:
        timestamp (Optional[int]): Timestamp of signal measure of type Timestamp in milliseconds
        start_timestamp (Optional[int]): Timestamp of begin signal measure of type Epoch in milliseconds
        end_timestamp (Optional[int]): Timestamp of end signal measure of type Epoch in milliseconds
        value (Union[str, float]): Value of signal
    """
    timestamp: Optional[int]
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    value: Union[str, float]


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
        signal_values (List[SignalIn]): list of signals
        additional_properties (Optional[List[PropertyIn]]): Additional properties for signal
    """
    type: Type
    source: Optional[str]
    signal_values: List[SignalIn] = []
    additional_properties: Optional[List[PropertyIn]]


class TimeSeriesTransformationIn(BaseModel):
    """
    Model of time series transformation to acquire from client

    Attributes:
        name (TransformationType): Name of the transformation
        source_time_series_ids (List[int]): Ids of source time series
        destination_observable_information_id (Optional[int]): Id of destination observable information
        destination_measure_id (Optional[int]): Id of destination measure
        additional_properties (Optional[List[PropertyIn]]): Additional properties for transformation
    """
    name: TransformationType
    source_time_series_ids: List[int]
    destination_observable_information_id: Optional[int]
    destination_measure_id: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class TimeSeriesTransformationRelationshipIn(BaseModel):
    """
    Model of time series transformation relationship

    Attributes:
        additional_properties (Optional[List[PropertyIn]]): Additional properties for transformation
    """
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
        signal_values (list): List of signal values
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    signal_values: list = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class TimeSeriesMultidimensionalOut(BaseModel):
    """
    Model of time multidimensional series to send to client as a result of request

    Attributes:
        signal_values (list): List of signal values
        time_series (List[TimeSeriesOut]): Time series nodes from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    signal_values: list = []
    time_series: List[TimeSeriesOut] = []
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
