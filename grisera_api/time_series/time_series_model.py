from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel

from models.base_model_out import BaseModelOut
from property.property_model import PropertyIn


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
    timestamp (int): Timestamp of signal measure of type Timestamp in milliseconds
    start_timestamp (int): Timestamp of begin signal measure of type Epoch in milliseconds
    end_timestamp (int): Timestamp of end signal measure of type Epoch in milliseconds
    value (SignalValueIn): Value of signal
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
    source (str): TimeSeries source
    signal_values (List[SignalIn]): list of signals
    additional_properties (Optional[List[PropertyIn]]): Additional properties for signal
    """

    type: Type
    source: Optional[str]
    signal_values: List[SignalIn] = []
    additional_properties: Optional[List[PropertyIn]]


class TimeSeriesRelationIn(BaseModel):
    """
    Model of time series relations to acquire from client

    Attributes:
    observable_information_id (Optional[Union[int, str]]): Id of observable information
    measure_id (Optional[Union[int, str]]): Id of measure
    """

    observable_information_id: Optional[Union[int, str]]
    measure_id: Optional[Union[int, str]]


class TimeSeriesIn(TimeSeriesPropertyIn, TimeSeriesRelationIn):
    """
    Full model of time series to acquire from client
    """


class BasicTimeSeriesOut(TimeSeriesPropertyIn):
    """
    Basic model of time series

    Attributes:
    id (Optional[Union[int, str]]): Id of time series returned from api
    """

    id: Optional[Union[int, str]]


class TimeSeriesOut(BasicTimeSeriesOut, BaseModelOut):
    """
    Model of time series with relations to send to client as a result of request

    Attributes:
    observable_informations (Optional[List[ObservableInformationOut]]): List of observable informations related to
        this time series
    measure (Optional[MeasureOut]): measure related to this time series
    """

    observable_informations: "Optional[List[ObservableInformationOut]]"
    measure: "Optional[MeasureOut]"


class TimeSeriesNodesOut(BaseModelOut):
    """
    Model of time series nodes to send to client as a result of request

    Attributes:
    time_series_nodes (List[BasicTimeSeriesOut]): Time series nodes from database
    """

    time_series_nodes: List[BasicTimeSeriesOut] = []


# circular import exeption prevention
from measure.measure_model import MeasureOut
from observable_information.observable_information_model import (
    ObservableInformationOut,
)

TimeSeriesOut.update_forward_refs()
